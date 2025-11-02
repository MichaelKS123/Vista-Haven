"""
Vista Haven - Airbnb Price Analysis
Created by Michael Semera

Comprehensive analysis of Airbnb listing prices and their influencing factors
Uses Python, Pandas, SQL, and visualization libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class VistaHavenAnalyzer:
    """
    Main class for Airbnb price analysis
    Handles data loading, cleaning, analysis, and visualization
    """
    
    def __init__(self, data_path=None):
        """Initialize the analyzer"""
        self.data_path = data_path
        self.df = None
        self.db_connection = None
        self.insights = {}
        
        # Set visualization style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['font.size'] = 10
        
        print("=" * 70)
        print("          🏠 VISTA HAVEN - Airbnb Price Analysis 🏠")
        print("                  Created by Michael Semera")
        print("=" * 70)
    
    def load_data(self, data_source='sample'):
        """
        Load Airbnb data from various sources
        
        Args:
            data_source: 'sample' for generated data, or path to CSV file
        """
        print("\n📊 Loading data...")
        
        if data_source == 'sample':
            self.df = self._generate_sample_data()
            print(f"✅ Generated {len(self.df)} sample listings")
        else:
            try:
                self.df = pd.read_csv(data_source)
                print(f"✅ Loaded {len(self.df)} listings from {data_source}")
            except Exception as e:
                print(f"❌ Error loading data: {e}")
                print("📝 Generating sample data instead...")
                self.df = self._generate_sample_data()
        
        return self.df
    
    def _generate_sample_data(self, n_listings=1000):
        """Generate realistic sample Airbnb data"""
        np.random.seed(42)
        
        # Cities with different price ranges
        cities = ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 
                 'Boston', 'Seattle', 'Austin', 'Miami']
        
        # Room types
        room_types = ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room']
        
        # Property types
        property_types = ['Apartment', 'House', 'Condo', 'Townhouse', 
                         'Loft', 'Villa', 'Cottage']
        
        # Neighborhoods (generic)
        neighborhoods = ['Downtown', 'Midtown', 'Uptown', 'Waterfront', 
                        'Historic District', 'Arts District', 'Business District']
        
        data = []
        
        for i in range(n_listings):
            city = np.random.choice(cities)
            room_type = np.random.choice(room_types, p=[0.5, 0.35, 0.1, 0.05])
            property_type = np.random.choice(property_types)
            neighborhood = np.random.choice(neighborhoods)
            
            # Base price influenced by city
            city_multipliers = {
                'New York': 1.5, 'San Francisco': 1.4, 'Los Angeles': 1.2,
                'Boston': 1.3, 'Seattle': 1.2, 'Chicago': 1.0,
                'Austin': 0.9, 'Miami': 1.1
            }
            base_price = 100 * city_multipliers.get(city, 1.0)
            
            # Adjust by room type
            if room_type == 'Entire home/apt':
                base_price *= 1.5
            elif room_type == 'Private room':
                base_price *= 0.7
            elif room_type == 'Shared room':
                base_price *= 0.4
            elif room_type == 'Hotel room':
                base_price *= 1.2
            
            # Other factors
            bedrooms = np.random.randint(1, 6)
            bathrooms = np.random.choice([1, 1.5, 2, 2.5, 3], p=[0.3, 0.25, 0.25, 0.15, 0.05])
            accommodates = bedrooms * 2 + np.random.randint(0, 3)
            
            # Reviews and ratings
            number_of_reviews = np.random.poisson(20)
            review_scores_rating = np.random.uniform(3.5, 5.0) if number_of_reviews > 0 else None
            
            # Amenities
            num_amenities = np.random.randint(5, 25)
            has_wifi = np.random.choice([True, False], p=[0.95, 0.05])
            has_kitchen = np.random.choice([True, False], p=[0.8, 0.2])
            has_parking = np.random.choice([True, False], p=[0.6, 0.4])
            has_pool = np.random.choice([True, False], p=[0.2, 0.8])
            
            # Host attributes
            host_is_superhost = np.random.choice([True, False], p=[0.3, 0.7])
            host_listings_count = np.random.choice([1, 2, 3, 5, 10], p=[0.5, 0.2, 0.15, 0.1, 0.05])
            instant_bookable = np.random.choice([True, False], p=[0.6, 0.4])
            
            # Minimum nights
            minimum_nights = np.random.choice([1, 2, 3, 7, 30], p=[0.5, 0.2, 0.15, 0.1, 0.05])
            
            # Calculate final price with noise
            price = base_price
            price += bedrooms * 30
            price += bathrooms * 20
            price += num_amenities * 2
            price += 20 if has_wifi else 0
            price += 30 if has_kitchen else 0
            price += 25 if has_parking else 0
            price += 40 if has_pool else 0
            price += 30 if host_is_superhost else 0
            price += (review_scores_rating - 4) * 30 if review_scores_rating else 0
            
            # Add random noise
            price *= np.random.uniform(0.85, 1.15)
            price = max(30, round(price, 2))
            
            # Availability
            availability_365 = np.random.randint(0, 366)
            
            data.append({
                'listing_id': i + 1,
                'city': city,
                'neighborhood': neighborhood,
                'property_type': property_type,
                'room_type': room_type,
                'accommodates': accommodates,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'price': price,
                'minimum_nights': minimum_nights,
                'number_of_reviews': number_of_reviews,
                'review_scores_rating': review_scores_rating,
                'host_is_superhost': host_is_superhost,
                'host_listings_count': host_listings_count,
                'instant_bookable': instant_bookable,
                'availability_365': availability_365,
                'num_amenities': num_amenities,
                'has_wifi': has_wifi,
                'has_kitchen': has_kitchen,
                'has_parking': has_parking,
                'has_pool': has_pool
            })
        
        return pd.DataFrame(data)
    
    def clean_data(self):
        """Clean and prepare data for analysis"""
        print("\n🧹 Cleaning data...")
        
        initial_count = len(self.df)
        
        # Handle missing values
        self.df['review_scores_rating'].fillna(self.df['review_scores_rating'].median(), inplace=True)
        
        # Remove outliers (prices > 99th percentile or < 1st percentile)
        q01 = self.df['price'].quantile(0.01)
        q99 = self.df['price'].quantile(0.99)
        self.df = self.df[(self.df['price'] >= q01) & (self.df['price'] <= q99)]
        
        # Convert boolean columns
        bool_columns = ['host_is_superhost', 'instant_bookable', 'has_wifi', 
                       'has_kitchen', 'has_parking', 'has_pool']
        for col in bool_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(int)
        
        print(f"✅ Cleaned data: {initial_count} → {len(self.df)} listings")
        print(f"   Removed {initial_count - len(self.df)} outliers/invalid records")
        
        return self.df
    
    def create_database(self):
        """Create SQLite database for SQL analysis"""
        print("\n🗄️  Creating SQLite database...")
        
        self.db_connection = sqlite3.connect(':memory:')
        self.df.to_sql('listings', self.db_connection, index=False, if_exists='replace')
        
        print("✅ Database created successfully")
        return self.db_connection
    
    def perform_exploratory_analysis(self):
        """Comprehensive exploratory data analysis"""
        print("\n🔍 Performing Exploratory Data Analysis...")
        print("=" * 70)
        
        # Basic statistics
        print("\n📊 Dataset Overview:")
        print(f"   Total listings: {len(self.df):,}")
        print(f"   Cities covered: {self.df['city'].nunique()}")
        print(f"   Room types: {self.df['room_type'].nunique()}")
        print(f"   Property types: {self.df['property_type'].nunique()}")
        
        # Price statistics
        print("\n💰 Price Statistics:")
        print(f"   Mean price: ${self.df['price'].mean():.2f}")
        print(f"   Median price: ${self.df['price'].median():.2f}")
        print(f"   Std deviation: ${self.df['price'].std():.2f}")
        print(f"   Min price: ${self.df['price'].min():.2f}")
        print(f"   Max price: ${self.df['price'].max():.2f}")
        
        # Price by city
        print("\n🌆 Average Price by City:")
        city_prices = self.df.groupby('city')['price'].agg(['mean', 'median', 'count'])
        city_prices = city_prices.sort_values('mean', ascending=False)
        for city, row in city_prices.iterrows():
            print(f"   {city:20s} Mean: ${row['mean']:7.2f} | Median: ${row['median']:7.2f} | Listings: {int(row['count']):4d}")
        
        # Price by room type
        print("\n🏠 Average Price by Room Type:")
        room_prices = self.df.groupby('room_type')['price'].agg(['mean', 'median', 'count'])
        room_prices = room_prices.sort_values('mean', ascending=False)
        for room_type, row in room_prices.iterrows():
            print(f"   {room_type:20s} Mean: ${row['mean']:7.2f} | Median: ${row['median']:7.2f} | Listings: {int(row['count']):4d}")
        
        # Store insights
        self.insights['city_prices'] = city_prices
        self.insights['room_prices'] = room_prices
        
        return self.insights
    
    def perform_sql_analysis(self):
        """Perform SQL queries for deeper analysis"""
        print("\n🔎 Performing SQL Analysis...")
        print("=" * 70)
        
        if self.db_connection is None:
            self.create_database()
        
        # Query 1: Top 10 most expensive cities
        print("\n1️⃣  Top 10 Most Expensive Cities:")
        query1 = """
        SELECT city, 
               ROUND(AVG(price), 2) as avg_price,
               COUNT(*) as num_listings
        FROM listings
        GROUP BY city
        ORDER BY avg_price DESC
        LIMIT 10
        """
        result1 = pd.read_sql_query(query1, self.db_connection)
        print(result1.to_string(index=False))
        
        # Query 2: Price correlation with amenities
        print("\n2️⃣  Impact of Amenities on Price:")
        query2 = """
        SELECT 
            CASE WHEN has_wifi = 1 THEN 'With WiFi' ELSE 'No WiFi' END as wifi_status,
            ROUND(AVG(price), 2) as avg_price
        FROM listings
        GROUP BY has_wifi
        UNION ALL
        SELECT 
            CASE WHEN has_kitchen = 1 THEN 'With Kitchen' ELSE 'No Kitchen' END as kitchen_status,
            ROUND(AVG(price), 2) as avg_price
        FROM listings
        GROUP BY has_kitchen
        UNION ALL
        SELECT 
            CASE WHEN has_pool = 1 THEN 'With Pool' ELSE 'No Pool' END as pool_status,
            ROUND(AVG(price), 2) as avg_price
        FROM listings
        GROUP BY has_pool
        """
        result2 = pd.read_sql_query(query2, self.db_connection)
        print(result2.to_string(index=False))
        
        # Query 3: Superhost premium
        print("\n3️⃣  Superhost Price Premium:")
        query3 = """
        SELECT 
            CASE WHEN host_is_superhost = 1 THEN 'Superhost' ELSE 'Regular Host' END as host_type,
            ROUND(AVG(price), 2) as avg_price,
            COUNT(*) as num_listings
        FROM listings
        GROUP BY host_is_superhost
        """
        result3 = pd.read_sql_query(query3, self.db_connection)
        print(result3.to_string(index=False))
        
        # Query 4: Bedroom analysis
        print("\n4️⃣  Price by Number of Bedrooms:")
        query4 = """
        SELECT bedrooms,
               ROUND(AVG(price), 2) as avg_price,
               COUNT(*) as num_listings
        FROM listings
        WHERE bedrooms <= 5
        GROUP BY bedrooms
        ORDER BY bedrooms
        """
        result4 = pd.read_sql_query(query4, self.db_connection)
        print(result4.to_string(index=False))
        
        return {
            'expensive_cities': result1,
            'amenity_impact': result2,
            'superhost_premium': result3,
            'bedroom_analysis': result4
        }
    
    def correlation_analysis(self):
        """Analyze correlations between features and price"""
        print("\n📈 Correlation Analysis...")
        
        # Select numeric columns
        numeric_cols = ['price', 'accommodates', 'bedrooms', 'bathrooms', 
                       'minimum_nights', 'number_of_reviews', 'review_scores_rating',
                       'host_listings_count', 'availability_365', 'num_amenities']
        
        correlation_matrix = self.df[numeric_cols].corr()
        price_corr = correlation_matrix['price'].sort_values(ascending=False)
        
        print("\n🔗 Features Most Correlated with Price:")
        for feature, corr in price_corr.items():
            if feature != 'price':
                print(f"   {feature:25s}: {corr:+.4f}")
        
        return correlation_matrix
    
    def build_price_prediction_model(self):
        """Build machine learning model to predict prices"""
        print("\n🤖 Building Price Prediction Model...")
        
        # Prepare features
        feature_cols = ['accommodates', 'bedrooms', 'bathrooms', 'num_amenities',
                       'host_is_superhost', 'instant_bookable', 'has_wifi', 
                       'has_kitchen', 'has_parking', 'has_pool', 'number_of_reviews',
                       'review_scores_rating']
        
        X = self.df[feature_cols].copy()
        y = self.df['price'].copy()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Evaluate
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        print(f"\n📊 Model Performance:")
        print(f"   R² Score: {r2:.4f}")
        print(f"   RMSE: ${rmse:.2f}")
        print(f"   Mean Absolute Error: ${np.mean(np.abs(y_test - y_pred)):.2f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\n🎯 Top Feature Importances:")
        for idx, row in feature_importance.head(10).iterrows():
            print(f"   {row['feature']:25s}: {row['importance']:.4f}")
        
        return model, feature_importance
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\n📊 Creating visualizations...")
        
        fig = plt.figure(figsize=(20, 12))
        
        # 1. Price distribution
        ax1 = plt.subplot(2, 3, 1)
        self.df['price'].hist(bins=50, edgecolor='black', alpha=0.7)
        ax1.set_title('Price Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Price ($)')
        ax1.set_ylabel('Frequency')
        ax1.axvline(self.df['price'].mean(), color='red', linestyle='--', 
                   label=f'Mean: ${self.df["price"].mean():.2f}')
        ax1.legend()
        
        # 2. Price by city
        ax2 = plt.subplot(2, 3, 2)
        city_avg = self.df.groupby('city')['price'].mean().sort_values(ascending=False)
        city_avg.plot(kind='barh', ax=ax2, color='steelblue')
        ax2.set_title('Average Price by City', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Average Price ($)')
        
        # 3. Price by room type
        ax3 = plt.subplot(2, 3, 3)
        self.df.boxplot(column='price', by='room_type', ax=ax3)
        ax3.set_title('Price Distribution by Room Type', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Room Type')
        ax3.set_ylabel('Price ($)')
        plt.suptitle('')
        
        # 4. Bedrooms vs Price
        ax4 = plt.subplot(2, 3, 4)
        bedroom_price = self.df.groupby('bedrooms')['price'].mean()
        bedroom_price.plot(kind='line', marker='o', ax=ax4, linewidth=2, markersize=8)
        ax4.set_title('Average Price by Number of Bedrooms', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Number of Bedrooms')
        ax4.set_ylabel('Average Price ($)')
        ax4.grid(True, alpha=0.3)
        
        # 5. Superhost impact
        ax5 = plt.subplot(2, 3, 5)
        superhost_data = self.df.groupby('host_is_superhost')['price'].mean()
        superhost_labels = ['Regular Host', 'Superhost']
        colors = ['#e74c3c', '#27ae60']
        ax5.bar(superhost_labels, superhost_data.values, color=colors, edgecolor='black')
        ax5.set_title('Superhost Price Premium', fontsize=14, fontweight='bold')
        ax5.set_ylabel('Average Price ($)')
        for i, v in enumerate(superhost_data.values):
            ax5.text(i, v + 5, f'${v:.2f}', ha='center', fontweight='bold')
        
        # 6. Amenities impact
        ax6 = plt.subplot(2, 3, 6)
        amenities = ['has_wifi', 'has_kitchen', 'has_parking', 'has_pool']
        amenity_impact = []
        for amenity in amenities:
            with_amenity = self.df[self.df[amenity] == 1]['price'].mean()
            without_amenity = self.df[self.df[amenity] == 0]['price'].mean()
            impact = with_amenity - without_amenity
            amenity_impact.append(impact)
        
        amenity_labels = ['WiFi', 'Kitchen', 'Parking', 'Pool']
        colors_amenity = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
        bars = ax6.barh(amenity_labels, amenity_impact, color=colors_amenity, edgecolor='black')
        ax6.set_title('Price Impact of Amenities', fontsize=14, fontweight='bold')
        ax6.set_xlabel('Price Difference ($)')
        for i, (bar, value) in enumerate(zip(bars, amenity_impact)):
            ax6.text(value + 1, i, f'${value:.2f}', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('vista_haven_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Visualization saved as 'vista_haven_analysis.png'")
        plt.show()
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "=" * 70)
        print("                    📋 VISTA HAVEN ANALYSIS REPORT")
        print("                      Created by Michael Semera")
        print("=" * 70)
        
        # Key findings
        print("\n🔑 KEY FINDINGS:")
        print("-" * 70)
        
        most_expensive_city = self.df.groupby('city')['price'].mean().idxmax()
        most_expensive_price = self.df.groupby('city')['price'].mean().max()
        
        print(f"\n1. Most Expensive City:")
        print(f"   {most_expensive_city} with average price of ${most_expensive_price:.2f}")
        
        entire_home_premium = (
            self.df[self.df['room_type'] == 'Entire home/apt']['price'].mean() -
            self.df[self.df['room_type'] == 'Private room']['price'].mean()
        )
        print(f"\n2. Room Type Impact:")
        print(f"   Entire homes cost ${entire_home_premium:.2f} more than private rooms on average")
        
        superhost_premium = (
            self.df[self.df['host_is_superhost'] == 1]['price'].mean() -
            self.df[self.df['host_is_superhost'] == 0]['price'].mean()
        )
        print(f"\n3. Superhost Premium:")
        print(f"   Superhosts charge ${superhost_premium:.2f} more on average")
        
        print(f"\n4. Size Matters:")
        bedroom_corr = self.df[['bedrooms', 'price']].corr().iloc[0, 1]
        print(f"   Bedrooms have a {bedroom_corr:.3f} correlation with price")
        print(f"   Each additional bedroom adds approximately ${self.df.groupby('bedrooms')['price'].mean().diff().mean():.2f}")
        
        # Recommendations
        print("\n" + "=" * 70)
        print("💡 RECOMMENDATIONS FOR HOSTS:")
        print("-" * 70)
        print("\n1. Pricing Strategy:")
        print("   • Set competitive prices based on your city's average")
        print("   • Consider premium pricing if you're a superhost")
        print("   • Price entire homes 50-100% higher than private rooms")
        
        print("\n2. Property Improvements:")
        print("   • Add valuable amenities (WiFi, Kitchen are essential)")
        print("   • Pool adds significant value in warm climates")
        print("   • Well-maintained spaces justify higher prices")
        
        print("\n3. Optimize Listings:")
        print("   • Achieve Superhost status for pricing power")
        print("   • Gather positive reviews to boost confidence")
        print("   • Keep availability calendar updated")
        
        print("\n" + "=" * 70)
        print("                    ✅ Analysis Complete!")
        print("=" * 70 + "\n")


def main():
    """Main execution function"""
    # Initialize analyzer
    analyzer = VistaHavenAnalyzer()
    
    # Load data
    analyzer.load_data('sample')
    
    # Clean data
    analyzer.clean_data()
    
    # Create database
    analyzer.create_database()
    
    # Perform analyses
    analyzer.perform_exploratory_analysis()
    analyzer.perform_sql_analysis()
    analyzer.correlation_analysis()
    analyzer.build_price_prediction_model()
    
    # Create visualizations
    analyzer.create_visualizations()
    
    # Generate final report
    analyzer.generate_report()
    
    print("\n📁 Outputs generated:")
    print("   ✓ vista_haven_analysis.png - Comprehensive visualizations")
    print("   ✓ Console output - Detailed analysis results")
    print("\n🎉 Thank you for using Vista Haven!")
    print("   Created by Michael Semera\n")


if __name__ == "__main__":
    main()