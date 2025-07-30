import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from Load_Data import Loader
from Data_Cleaning import Cleaner
from Analysis import BookDataAnalysis,CorrelationAnalysis,Reccomandation_Models
from Data_Visualization import Plots
import pandas as pd

filename = r"C:\\Users\\lenovo\\Documents\\analytics\\Amazon_Books_Data\\Amazon_popular_books_dataset.csv"

output_path1 = r"C:\\Users\\lenovo\\Documents\\analytics\\Amazon_Books_Data\\src\\Data_Cleaning"

save_dir = "C:\\Users\\lenovo\\Documents\\analytics\\Amazon_Books_Data\\src\\Data_Visualization"
# Load the dataset
df = Loader.load_dataset(filename)

# Show missing values
missing_values = Cleaner.show_nan(df)
print(missing_values)

# Delete unnecessary columns
Cleaner.delete_columns(df)

# Handle missing values in the price column
df = Cleaner.handle_price(df)


#Handle missing values in the number_of_sellers column
df = Cleaner.handle_number_of_sellers(df)

#Handle missing values in the format column
df = Cleaner.handle_format(df)


#handle the missing values in the columns item_weight,root_bs_rank,brand,best_sellers_rank
df = Cleaner.handle_other_columns(df)

print("\nDataframe after handling  columns:\n")
missing_values = Cleaner.show_nan(df)
print(missing_values)

#parse item_weight from 'pounds|ounces' to grams
df = Cleaner.parse_item_weight(df)
print(df['item_weight'].head(5))

#handle column best_sellers_rank
df = Cleaner.handle_best_sellers_rank(df)



df = Cleaner.add_stock_columns(df)


df = Cleaner.get_book_format(df)

df = Cleaner.handle_book_fomat(df)

df = Cleaner.handle_timestamp(df)

df = Cleaner.handle_rating(df)

df = Cleaner.handle_categories(df)

#normalize dataframe for the reccomandation models
df_norm = Reccomandation_Models.data_preprocessing(df)

#test the method filter_by_asin to reccomend top 10 books in the same category as the book with asin code 0060244887
print("\nReccomandations by rating:")
reccomandations = Reccomandation_Models.filter_by_category(df_norm,'0062024027',10)
if not reccomandations.empty:
    print(reccomandations.to_string(index = False))
else:
    print("No reccomandations available") 
    
#test the model knn_category_recommender
print("\nNearest Neighbors Model:")
reccomandations = Reccomandation_Models.knn_category_recommender(df_norm,'0060244887',10)
if not reccomandations.empty:
    print(reccomandations.to_string(index = False))
else:
    print("No reccomandations available") 
    
#test the model kmeans_reccomender
print("\nKMeans reccomandation model:")
recs = Reccomandation_Models.kmeans_reccomender(df_norm, '0060244887', num_recs = 10)
print(recs)


#exploratory analysis
top10_popular = BookDataAnalysis.top10_most_popular(df)
print("\nTop 10 Most Popular Books:\n", top10_popular)

top10_discounted = BookDataAnalysis.top10_discounted_products(df)
print("\nTop 10 discounted books:\n", top10_discounted)

avg_discount = BookDataAnalysis.avg_discount_per_category(df)
print("\nAverage discount per category:\n", avg_discount)

avg_discount_format = BookDataAnalysis.avg_discount_per_format(df)
print("\nAverage discount per book format:\n", avg_discount_format)

avg_discount_rating = BookDataAnalysis.avg_discount_per_rating(df)
print("\nAverage discount per rating:\n", avg_discount_rating)

avg_discount_rating_count = BookDataAnalysis.avg_discount_per_rating_count(df)
print("\nAverage discount per rating count:\n", avg_discount_rating_count)

discount_availability = BookDataAnalysis.discount_vs_availability(df)
print("\nDiscount vs Availability:\n", discount_availability)


top10_cheapest = BookDataAnalysis.top10_cheapest_per_category(df)
print("\nTop 10 cheapest categories books:\n", top10_cheapest)
top10_expensive = BookDataAnalysis.top10_most_expensive_category(df)
print("\nTop 10 most expensive categories books:\n", top10_expensive)

top10_best_sellers = BookDataAnalysis.top10_bestsellers(df)
print("\nTop 10 best sellers:\n", top10_best_sellers)

print("\nTop 10 most reviewed books:\n")
top10_reviewed = BookDataAnalysis.top10_most_rated(df)
print(top10_reviewed)

print("\nNumber of books in each category:\n")
num_books = BookDataAnalysis.books_per_category(df)
print(num_books)

print("\nAvailability vs Price:")
availability_vs_price = BookDataAnalysis.availability_vs_price(df)
print(availability_vs_price)


print("\nAverage price per rating count:\n")
avg_price_rating_count = BookDataAnalysis.reviews_count_vs_price(df)
print(avg_price_rating_count)

print("\nAverage price per seller:\n")
avg_price_per_seller = BookDataAnalysis.avg_price_per_seller(df)
print(avg_price_per_seller)

print("\nTop 10 sellers with most books in stock:\n")
num_books_per_seller = BookDataAnalysis.num_books_per_seller(df)
print(num_books_per_seller)


unique_ranges = df['num_reviews_range'].unique()
print("Range recensioni:", unique_ranges)


Plots.top10_discounted_titles(df,save_dir)
Plots.top10_cheapest_categories(df,save_dir)
Plots.top10_expensive_categories(df,save_dir)
Plots.top10_sellers(df,save_dir)
Plots.categories_vs_rating(df,save_dir)
Plots.rank_vs_titles(df,save_dir)
Plots.format_vs_rating(df, save_dir)
Plots.top10_most_reviewed(df,save_dir)
Plots.histogram_reviews(df,save_dir)
Plots.histogram_rating(df,save_dir)
Plots.histogram_price(df,save_dir)
Plots.reviews_range_vs_price(df,save_dir)
Plots.show_book_availability(df,save_dir)
Plots.show_not_available_titles(df,save_dir)

print("\nLinear correlation between numerical columns:\n")
correlation = CorrelationAnalysis.numerical_variables_correlation(df)
print(correlation)

CorrelationAnalysis.cramers_v_heatmap(df)

print("\nMost significant differences across categories and rating groups:\n")
categories_rating_variability = CorrelationAnalysis.categories_vs_rating(df)
if categories_rating_variability is not None:
    print(categories_rating_variability)
    
print("\nMost significant differences across 'brand' and 'final_price' groups:\n")
brand_price_variability = CorrelationAnalysis.brand_vs_price(df)
if brand_price_variability is not None:
    print(brand_price_variability)
    
print("\nMost significant difference across 'book_format' and 'rating' groups:\n")
bookformat_rating_variability = CorrelationAnalysis.bookformat_vs_rating(df)
if bookformat_rating_variability is not None:
    print(bookformat_rating_variability)
    
print("\nMost significant differences across 'book_format' and 'final_price' groups:\n")
categories_price_variability = CorrelationAnalysis.bookformat_vs_price(df)
if categories_price_variability is not None:
    print(categories_price_variability)
    
print("\nMost significant differences across 'book_format' and 'discount_pct' groups:\n")
format_discount_variability = CorrelationAnalysis.bookformat_vs_discount(df)
if format_discount_variability is not None:
    print(format_discount_variability)
    
print("\nMost significant differences across 'brand' and 'rating' groups:\n")
brand_rating_variability = CorrelationAnalysis.brand_vs_rating(df)
if brand_rating_variability is not None:
    print(brand_rating_variability)
    
print("\nMost significant differences across seller_name and final_price groups:\n")
sellername_price_variability = CorrelationAnalysis.sellername_vs_price(df)
if sellername_price_variability is not None:
    print(sellername_price_variability)
    
    

#save the new dataframe in the folder Data_Cleaning
df.to_csv(os.path.join(output_path1, "cleaned_data.csv"), index=False)
