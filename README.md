Project Overview
This project aims to compare the prices of products available on the Government e-Marketplace (GeM) with those on other popular e-commerce platforms such as Amazon and Flipkart. The tool helps users analyze pricing trends, identify cost-effective purchasing options, and make informed decisions.

 Features
- Scrapes product details from GeM, Amazon, and Flipkart.
- Compares product prices across these platforms.
- Displays the results in an easy-to-understand format.
- Provides insights into pricing differences and trends.
- Helps in decision-making for government procurement and general users.

 Technologies Used
- Python: Core programming language.
- BeautifulSoup & Selenium: For web scraping.
- Flask: Web framework for creating the application.
- SQLite/MySQL: Database for storing product details.
- HTML, CSS, JavaScript: For frontend development.
- TailwindCSS: For responsive and modern UI design.

 Installation & Setup
 Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- Google Chrome & ChromeDriver (if using Selenium)

 Steps to Install
1.Run the application:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

Usage
1. Enter the product name in the search bar.
2. Select the platforms you want to compare (GeM, Amazon, Flipkart).
3. Click on "Compare" to get a detailed price analysis.
4. View the results and choose the best deal.

Future Enhancements
- Implement AI-based price prediction.
- Add more e-commerce platforms.
- Improve data accuracy with enhanced scraping techniques.
- Provide historical price tracking.

Contributors
- Abhishek Veerappa Magalada

License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
