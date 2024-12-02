import matplotlib.pyplot as plt
import pandas as pd
import statistics
import seaborn as sns

RESULTS = pd.read_csv('data/csvData.csv', index_col=0)

def pages_per_website():
    results = RESULTS

    websites = results["Website"].to_list()
    num_pages = results["Number of Pages"].to_list()

    plt.figure(figsize=(20, 8))
    plt.bar(websites, num_pages, color='blue')
    plt.title("Number of Pages per Website")
    plt.xlabel("Website")
    plt.ylabel("Number of Pages")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/number_of_pages.png", dpi=300)
    plt.close()

def ccokies_per_website():
    results = RESULTS

    websites = results["Website"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    plt.figure(figsize=(20, 8))
    plt.bar(websites, num_cookies, color='green')
    plt.title("Number of Cookies per Website")
    plt.xlabel("Website")
    plt.ylabel("Number of Cookies")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/number_of_cookies.png", dpi=300)
    plt.close()

def avg_pages_cookies_by_category():
    results = RESULTS

    websites = results["Website"].to_list()
    num_pages = results["Number of Pages"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    luxury_clothing_sites = websites[:25]
    fast_fashion_sites = websites[25:50]
    tech_sites = websites[50:75]
    vehicle_sites = websites[75:]

    luxury_clothing_pages = num_pages[:25]
    fast_fashion_pages = num_pages[25:50]
    tech_pages = num_pages[50:75]
    vehicle_pages = num_pages[75:]

    luxury_clothing_cookies = num_pages[:25]
    fast_fashion_cookies = num_pages[25:50]
    tech_cookies = num_pages[50:75]
    vehicle_cookies = num_pages[75:]

    luxury_avg_pages = statistics.mean(luxury_clothing_pages)
    fast_avg_pages = statistics.mean(fast_fashion_pages)
    tech_avg_pages = statistics.mean(tech_pages)
    vehicle_avg_pages = statistics.mean(vehicle_pages)

    luxury_avg_cookies = statistics.mean(luxury_clothing_cookies)
    fast_avg_cookies = statistics.mean(fast_fashion_cookies)
    tech_avg_cookies = statistics.mean(tech_cookies)
    vehicle_avg_cookies = statistics.mean(vehicle_cookies)

    avg_pages = [luxury_avg_pages, fast_avg_pages, tech_avg_pages, vehicle_avg_pages]
    avg_cookies = [luxury_avg_cookies, fast_avg_cookies, tech_avg_cookies, vehicle_avg_cookies]

    categories = ["Luxury Clothing Brands", "Fast Fashion Clothing Brands", "Technology Brands", "Vehicle Brands"]
    
    # Create the scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    plt.scatter(avg_pages, avg_cookies)


    # Add labels and title
    plt.xlabel('Average Number of Pages')
    plt.ylabel('Average Number of Cookies')
    plt.title('Average Number of Pages to Cookies by Website Category')

    for i, category in enumerate(categories):
        ax.txt(avg_pages[i], avg_cookies[i], category)


    plt.tight_layout()
    plt.savefig("analysis/avg_pages_to_cookies_by_category.png", dpi=300)
    plt.close()

def pages_cookies_by_category():
    results = RESULTS

    websites = results["Website"].to_list()
    num_pages = results["Number of Pages"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    categories = ["Luxury Clothing Brands", "Fast Fashion Clothing Brands", "Technology Brands", "Vehicle Brands"]

    luxury_clothing_sites = websites[:25]
    fast_fashion_sites = websites[25:50]
    tech_sites = websites[50:75]
    vehicle_sites = websites[75:]

    luxury_clothing_pages = num_pages[:25]
    fast_fashion_pages = num_pages[25:50]
    tech_pages = num_pages[50:75]
    vehicle_pages = num_pages[75:]

    luxury_clothing_cookies = num_pages[:25]
    fast_fashion_cookies = num_pages[25:50]
    tech_cookies = num_pages[50:75]
    vehicle_cookies = num_pages[75:]

    # Combine data for pages and cookies into DataFrame
    page_data = pd.DataFrame({
        "Category": categories[0] * 25 + categories[1] * 25 + categories[2] * 25 + categories[3] * 25,
        "Metric": ["Number of Pages"] * 100,
        "Value": luxury_clothing_pages + fast_fashion_pages + tech_pages + vehicle_pages
    })

    cookie_data = pd.DataFrame({
        "Category": categories[0] * 25 + categories[1] * 25 + categories[2] * 25 + categories[3] * 25,
        "Metric": ["Number of Cookies"] * 100,
        "Value": luxury_clothing_cookies + fast_fashion_cookies + tech_cookies + vehicle_cookies
    })

    combined_data = pd.concat([page_data, cookie_data])

    # Plot the violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=combined_data, x="Category", y="Value", hue="Metric", split=True)
    plt.title("Distribution of Pages and Cookies by Category")
    plt.ylabel("Value")
    plt.xlabel("Category")
    plt.legend(title="Metric")
    plt.tight_layout()

    plt.savefig("analysis/violin_plot_pages_cookies_by_category.png", dpi=300)
    plt.close()


    
def page_cookie_correlation():
    results = RESULTS
    websites = results["Website"].to_list()
    num_pages = results["Number of Pages"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    corr, _ = pearsonr(num_pages, num_cookies)

    # Scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(num_pages, num_cookies, alpha=0.7, color='blue', edgecolor='k')

    # Add labels and title
    plt.xlabel("Number of Pages")
    plt.ylabel("Number of Cookies")
    plt.title("Correlation Between Number of Pages and Number of Cookies")
    plt.grid(True)

    # Display correlation coefficient on the plot
    plt.text(
        0.05, 0.95, 
        f"Pearson r = {corr:.2f}",
        fontsize=12,
        ha='left',
        va='center',
        transform=plt.gca().transAxes,
        bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray')
    )


    # Annotate points with website names (optional)
    for website, x, y in zip(websites, num_pages, num_cookies):
        plt.text(x, y, website, fontsize=8, alpha=0.7)

    plt.tight_layout()
    plt.savefig("analysis/page_cookie_correlation.png", dpi=300)
    plt.close()

def mixed_content():
    results = RESULTS
    websites = results["Website"].to_list()
    mixed_content = results["Mixed Content"].to_list()

    mixed_pages = [num_pages[i] for i in range(len(mixed_content)) if mixed_content[i] == "True"]
    not_mixed_pages = [num_pages[i] for i in range(len(mixed_content)) if mixed_content[i] == "False"]

    mixed = mixed_content.count("True")
    not_mixed = mixed_content.count("False")
    unavailable = mixed_content.count("Denied")

    categories = ["Mixed Content", "Not Mixed Content", "Unavailable"]
    counts = [mixed, not_mixed, unavailable]

    t_stat, p_value = ttest_ind(mixed_pages, not_mixed_pages, equal_var=False)

    # Annotate bars with p-value or significance stars
    if p_value < 0.001:
        significance = "***"
    elif p_value < 0.01:
        significance = "**"
    elif p_value < 0.05:
        significance = "*"
    else:
        significance = "n.s."  # not significant

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, counts, color=["blue", "red", "gray"])

    max_y = max(counts)
    x1, x2 = 0, 1  # Positions of the first two bars
    y, h = max_y * 1.05, max_y * 0.03  # Height of the line and text
    plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color="black")
    plt.text((x1 + x2) / 2, y + h * 1.2, f"p = {p_value:.3e} ({significance})", ha='center', fontsize=12)

    plt.title("Websites that use HTTP, HTTPS, or Mixed Content")
    plt.xlabel("Website")
    plt.ylabel("Content Type (Mixed, Not Mixed, or Unavailable)")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.ylim(0, max_y * 1.2)
    plt.tight_layout()
    plt.savefig("analysis/mixed_content_significance.png", dpi=300)
    plt.close()

def num_dnsmpi_links():

    results = RESULTS

    websites = results["Website"].to_list()
    dnsmpi_content = results["Contains DNSMPI-associated Content?"].to_list()

    categories = ["Has DNSMPI content", "Does not have DNSMPI content"]
    dnsmpi = dnsmpi_content.count("Yes")
    no_dnsmpi = dnsmpi_content.count("No")
    data = [dnsmpi, no_dnsmpi]

    plt.figure(figsize=(20, 8))
    plt.bar(categories, data, color=['blue', 'red'])
    plt.title("DNSMPI Content")
    plt.xlabel("Has Content")
    plt.ylabel("Number of Websites")
    plt.xticks(ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/number_of_dnsmpi_links.png", dpi=300)
    plt.close()

def cookies_to_dnsmpi_links():
    results = RESULTS

    websites = results["Website"].to_list()
    dnsmpi_content = results["Contains DNSMPI-associated Content?"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x=dnsmpi_content, y=num_cookies, palette="Set2")

    plt.title('Cookie Number by DNSMPI Status')
    plt.xlabel('DNSMPI Status')
    plt.ylabel('Number of Cookies')

def summary_statistics():
    results = RESULTS
    summary_stats = results.describe())

def correlation_matrix(column1, column2):
    results = RESULTS
    corr_matrix = results[[column1, column2]].corr()