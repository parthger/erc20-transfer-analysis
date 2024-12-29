
import requests  # To interact with the Dune API
import pandas as pd  # handle and process data
import matplotlib.pyplot as plt  # For plotting graphs
import seaborn as sns  # for visualizations
import time  
from typing import Dict, Any 

def fetch_dune_data(api_key: str, query_id: str) -> pd.DataFrame:
    """
    Fetch transaction data from the Dune Analytics API.
    
    Args:
        api_key (str): Your Dune API key to authenticate requests. Most important got stuck here for 2 hours to find out how to do it.
        query_id (str): The query ID to execute on Dune.

    
    
    Workflow:
    1. Send a request to Dune to execute a query.
    2. Wait for Dune to process and complete the query.
    3. Once complete, fetch the results as a DataFrame.
    """
    base_url = "https://api.dune.com/api/v1/"
    headers = {"X-Dune-API-Key": api_key}
    
    try:
        # Step 1: Execute the query
        print("Starting query execution...")
        execute_endpoint = f"{base_url}query/{query_id}/execute"
        execution_response = requests.post(execute_endpoint, headers=headers)
        
        # Checking th execution request 
        if execution_response.status_code != 200:
            raise Exception(f"Query execution failed: {execution_response.text}")
            
        # Extract execution ID 
        execution_id = execution_response.json()["execution_id"]
        print(f"Execution ID: {execution_id}")
        
        # Step 2: Monitor the query 
        status_endpoint = f"{base_url}execution/{execution_id}/status"
        while True:
            status_response = requests.get(status_endpoint, headers=headers)
            state = status_response.json()["state"]
            print(f"Current status: {state}")
            
           
            if state == "QUERY_STATE_COMPLETED":
                break
            elif state == "QUERY_STATE_FAILED":
                raise Exception("Query execution failed")
                
           
            time.sleep(5)
        
        # Step 3: Fetching results
        print("Fetching results...")
        results_endpoint = f"{base_url}execution/{execution_id}/results"
        results_response = requests.get(results_endpoint, headers=headers)
        
        if results_response.status_code != 200:
            raise Exception(f"Failed to fetch results: {results_response.text}")
            
        # Converting JSON into a Pandas DataFrame
        df = pd.DataFrame(results_response.json()["result"]["rows"])
        print("Data retrieved successfully!")
        return df
    
    except Exception as e:
        
        print(f"Error: {str(e)}")
        raise


# Replace QUERY_ID and API_KEY with your actual values from Dune.
QUERY_ID = "4493349"
API_KEY = "vTIUROGky07AVY5gWXB18vo7j5uiQBT9"

try:
    print("Starting Dune data fetch...")
    df = fetch_dune_data(API_KEY, QUERY_ID)
    df.to_csv("dune_transactions.csv", index=False)  # Saving data for future use.
    print("Data saved to 'dune_transactions.csv'")
except Exception as e:
    print(f"Failed to fetch data: {str(e)}")

#  Data Preprocessing
# Load the saved data into a DataFrame
df = pd.read_csv("dune_transactions.csv")

# Ensure necessary columns are present
df['value'] = pd.to_numeric(df['value'], errors='coerce')  
df.dropna(subset=['from', 'to', 'value'], inplace=True)  # Removing unwanted colums without data

# Step 3: User Activity Analysis
def analyze_user_activity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze user activity based on transaction data.

    Args:
        df (pd.DataFrame): Transaction data.

    Returns:
        pd.DataFrame: User activity statistics (total transfers, max/min transaction values, unique tokens).
    """
    # Total number of transfers executed by each user
    user_activity = df.groupby('from').size().reset_index(name='total_transfers')
    
    # Maximum transaction amount for each user
    max_transaction = df.groupby('from')['value'].max().reset_index(name='max_transaction')

    # Minimum transaction amount for each user
    min_transaction = df.groupby('from')['value'].min().reset_index(name='min_transaction')

    # Count of unique tokens traded by each user (based on 'to' address)
    unique_tokens = df.groupby('from')['to'].nunique().reset_index(name='unique_tokens') #here i am assuming the "to" address to be token address as every uniwue token address will be a unique token

    
    user_stats = user_activity.merge(max_transaction, on='from')\
                              .merge(min_transaction, on='from')\
                              .merge(unique_tokens, on='from')

    return user_stats

# Generate statistics for user activity
user_stats = analyze_user_activity(df)
print("\nUser Statistics:")
print(user_stats.head())  # Display the first few rows for a quick look

# Step 4: Correlation Analysis
# This calculates how different features like total transfers, max transaction, etc., are related
correlation_matrix = user_stats[['total_transfers', 'max_transaction', 'min_transaction', 'unique_tokens']].corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Step 5: Visualizations
def create_visualizations(user_stats: pd.DataFrame, correlation_matrix: pd.DataFrame):
    """
    Create visualizations to showcase trends and correlations.

    Args:
        user_stats (pd.DataFrame): User statistics data.
        correlation_matrix (pd.DataFrame): Correlation matrix.
    """
    # Heatmap of correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix of User Activity')
    plt.show()

    # Histogram of total transfers
    plt.figure(figsize=(10, 6))
    sns.histplot(user_stats['total_transfers'], kde=True, color='blue', bins=20)
    plt.title('Distribution of Total Transfers per User')
    plt.xlabel('Total Transfers')
    plt.ylabel('Frequency')
    plt.show()

    # Histogram of max transaction amount
    plt.figure(figsize=(10, 6))
    sns.histplot(user_stats['max_transaction'], kde=True, color='green', bins=20)
    plt.title('Distribution of Max Transaction Amount per User')
    plt.xlabel('Max Transaction Amount')
    plt.ylabel('Frequency')
    plt.show()

 #visualizations to make the data more insightful
create_visualizations(user_stats, correlation_matrix)


user_stats.to_csv('user_statistics.csv', index=False)
print("\nUser statistics saved to 'user_statistics.csv'")
