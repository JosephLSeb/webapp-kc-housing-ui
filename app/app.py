#created By: Sebastian L
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# read the dataset
house_sales = pd.read_csv('kc_house_data.csv')

# define relevant filters
bedrooms_filter = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 33]
price_range_filter = [0, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000]


@app.route('/')
def home():
    #return render_template("home.html")
    return render_template('home.html', bedrooms_filter=bedrooms_filter, price_range_filter=price_range_filter)
    

@app.route('/analysis', methods=['POST'])
def analysis():
    # read the selected filters from the user
    bedrooms = request.form['bedrooms']
    price_range = request.form['price_range']

    # filter the dataset based on the selected filters
    filtered_sales = house_sales.loc[(house_sales['bedrooms'] == int(bedrooms)) &
                                     (house_sales['price'] >= price_range_filter[int(price_range)]) &
                                     (house_sales['price'] < price_range_filter[int(price_range) + 1])]

    # compute the required statistics
    volume_by_month = filtered_sales.groupby(pd.to_datetime(filtered_sales['date']).dt.to_period('M'))['price'].agg(['count', 'sum'])
    avg_price_by_month = filtered_sales.groupby(pd.to_datetime(filtered_sales['date']).dt.to_period('M'))[['price', 'sqft_living', 'bedrooms']].mean()
    
    # plot the statistics
    

    # Plot the Volume of Deals vs Time
    
    # Create a new Matplotlib Figure object with two subplots
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8, 8))

    # Plot the first subplot
    volume_by_month.plot(ax=ax1, y='count', legend=False, marker='o', markerfacecolor='red', markersize=10)
    ax1.set_title('Volume of Deals vs Time')
    ax1.set_ylabel('Volume of Deals (Number)')
    ax1.grid()

    # Plot the second subplot
    volume_by_month.plot(ax=ax2, y='sum', legend=False, marker='o', markerfacecolor='blue', markersize=10)
    ax2.set_title('Volume of Deals vs Total Amount')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Volume of Deals (Total Amount )')
    ax2.grid()

    # Adjust the spacing between subplots and save the figure
    fig.tight_layout()
    fig.savefig('figure1.png')

    # convert the plot to base64 string
    import io
    import base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    plot_url = base64.b64encode(buf.read()).decode('utf-8')

    
    # Plot the average price per unit over time
    
    # Create a new Matplotlib Figure object with three subplots
    fig2, (ax3, ax4, ax5) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(8, 12))

    # Plot the first subplot
    avg_price_by_month.plot(ax=ax3, y='price', legend=False, marker='o', markerfacecolor='cyan', markersize=10)
    ax3.set_title('Avg. Price per Deal vs Time')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Avg. Price per Deal ($)', color='r')
    ax3.grid()

    # Plot the second subplot
    avg_price_by_month.plot(ax=ax4, y='sqft_living', legend=False, marker='o', markerfacecolor='magenta', markersize=10)
    ax4.set_title('Avg. Price per Sqft vs Time')
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Avg. Price per Sqft')
    ax4.grid()

    # Plot the third subplot
    avg_price_by_month.plot(ax=ax5, y='bedrooms', legend=False, marker='o', markerfacecolor='green', markersize=10)
    ax5.set_title('Avg. Price per Bedroom vs Time')
    ax5.set_xlabel('Date')
    ax5.set_ylabel('Avg. Price per Bedroom')
    ax5.grid()

    # Adjust the spacing between subplots and save the figure
    fig2.tight_layout()
    fig2.savefig('figure2.png')

    # convert the plot to base64 string
    
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    buf2.seek(0)
    plot_url2 = base64.b64encode(buf2.read()).decode('utf-8')


    # render the analysis template with the computed statistics and plot
    return render_template('analysis.html', volume_by_month=volume_by_month.to_html(),
                           avg_price_by_month=avg_price_by_month.to_html(), plot_url=plot_url, plot_url2=plot_url2)



if __name__ == '__main__':
    app.run(debug=True)

