import matplotlib.pyplot as plt
import pandas as pd
import statistics
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import ttest_ind
from adjustText import adjust_text 
import ast

RESULTS = pd.read_csv('data/FinalTableData.csv', index_col=0)
COMPANY_NAMES = [site.split(".")[1] for site in RESULTS.index]


def pages_per_website():
    results = RESULTS

    websites = results.index.to_list()

    num_pages = results["Number of Pages"].to_list()

    plt.figure(figsize=(20, 8))
    plt.bar(COMPANY_NAMES, num_pages, color='cornflowerblue')
    plt.title("Number of Pages per Website")
    plt.xlabel("Website")
    plt.ylabel("Number of Pages")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/number_of_pages.png", dpi=300)
    plt.close()

def cookies_per_website():
    results = RESULTS

    websites = results.index.to_list()
    num_cookies = results["Number of Cookies"].to_list()

    plt.figure(figsize=(20, 8))
    plt.bar(COMPANY_NAMES, num_cookies, color='seagreen')
    plt.title("Number of Cookies per Website")
    plt.xlabel("Website")
    plt.ylabel("Number of Cookies")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/number_of_cookies.png", dpi=300)
    plt.close()

def avg_pages_cookies_by_category():
    results = RESULTS

    websites = results.index.to_list()
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

    categories = ["Luxury Clothing", "Fast Fashion", "Technology", "Vehicles"]
    
    # Create the scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    plt.scatter(avg_pages, avg_cookies)

    # Add labels and title
    plt.xlabel('Average Number of Pages')
    plt.ylabel('Average Number of Cookies')
    plt.title('Average Number of Pages to Cookies by Website Category')

    for i, category in enumerate(categories):
        ax.text(avg_pages[i], avg_cookies[i], category)


    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/avg_pages_to_cookies_by_category.png", dpi=300)
    plt.close()

def pages_cookies_by_category():
    results = RESULTS

    num_pages = results["Number of Pages"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    categories = ["Luxury Clothing", "Fast Fashion", "Technology", "Vehicles"]

    # Split data by category
    luxury_clothing_data = {"Category": ["Luxury Clothing"] * 25, 
                            "Pages": num_pages[:25], 
                            "Cookies": num_cookies[:25]}
    fast_fashion_data = {"Category": ["Fast Fashion"] * 25, 
                         "Pages": num_pages[25:50], 
                         "Cookies": num_cookies[25:50]}
    tech_data = {"Category": ["Technology"] * 25, 
                 "Pages": num_pages[50:75], 
                 "Cookies": num_cookies[50:75]}
    vehicle_data = {"Category": ["Vehicles"] * 25, 
                    "Pages": num_pages[75:], 
                    "Cookies": num_cookies[75:]}

    # Combine into a single DataFrame
    combined_data = pd.concat([
        pd.DataFrame(luxury_clothing_data),
        pd.DataFrame(fast_fashion_data),
        pd.DataFrame(tech_data),
        pd.DataFrame(vehicle_data),
    ], ignore_index=True)

    # Melt the data for Seaborn compatibility
    melted_data = combined_data.melt(
        id_vars=["Category"], 
        value_vars=["Pages", "Cookies"], 
        var_name="Metric", 
        value_name="Value"
    )

    # Plot the violin plots
    plt.figure(figsize=(12, 8))
    sns.violinplot(
        data=melted_data,
        x="Category",
        y="Value",
        hue="Metric",
        split=True,
        scale="width"
    )
    
    plt.title("Distribution of Pages and Cookies by Category")
    plt.ylabel("Value")
    plt.xlabel("Category")
    plt.legend(title="Metric")
    plt.tight_layout()

    # Save the plot
    plt.savefig("analysis/ImageFiles/violin_plot_pages_cookies_by_category.png", dpi=300)
    plt.close()

def page_cookie_correlation():
    results = RESULTS
    websites = results.index.to_list()
    num_pages = results["Number of Pages"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    corr, _ = pearsonr(num_pages, num_cookies)

    # Scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(num_pages, num_cookies, alpha=0.7, color='darkslategray', edgecolor='darkslategray')

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

    texts = []
    # Annotate points with website names (optional)
    for website, x, y in zip(COMPANY_NAMES, num_pages, num_cookies):
        text = plt.text(x, y, website, fontsize=9, alpha=0.8, ha='center', va='center')
        texts.append(text)

    # Adjust text to avoid overlap
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray'))

    # Tight layout for better spacing and saving the image
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/page_cookie_correlation.png", dpi=300)
    plt.close()

def mixed_content():
    results = RESULTS
    websites = results.index.to_list()
    mixed_content = results["Mixed Content"].to_list()

    
    mixed_pages = [num_pages[i] for i in range(len(mixed_content)) if mixed_content[i] == "True"]
    not_mixed_pages = [num_pages[i] for i in range(len(mixed_content)) if mixed_content[i] == "False"]

    mixed = mixed_content.count("TRUE")
    not_mixed = mixed_content.count("FALSE")
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
    bars = plt.bar(categories, counts, color=["mediumseagreen", "orchid", "silver"])

    max_y = max(counts)
    x1, x2 = 0, 1  # Positions of the first two bars
    y, h = max_y * 1.05, max_y * 0.03  # Height of the line and text
    plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color="black")
    plt.text((x1 + x2) / 2, y + h * 1.2, f"p = {p_value:.3e} ({significance})", ha='center', fontsize=12)

    plt.title("Websites that use Mixed Content")
    plt.xlabel("Website")
    plt.ylabel("Content Type (Mixed, Not Mixed, or Unavailable)")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.ylim(0, max_y * 1.2)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/mixed_content_significance.png", dpi=300)
    plt.close()

def protocol_content():
    results = RESULTS
    
    websites = results.index.to_list()
    protocol_content = results["HTTP/HTTPS Policies Category"].to_list()

    http = protocol_content.count("HTTP-Only")
    https = protocol_content.count("HTTPS-Only")
    both = protocol_content.count("both")
    neither = protocol_content.count("Neither")

    categories = ["HTTPS-Only","HTTP-Only","both", "Unavailable"]
    counts = [https,http,both,neither]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, counts, color=["silver", "mediumseagreen", "darkseagreen", "paleturquoise"])

    max_y = max(counts)
    x1, x2,= 0, 1  # Positions of the first two bars
    y, h = max_y * 1.05, max_y * 0.03  # Height of the line and text


    plt.title("Websites that use HTTPS,HTTP, or both")
    plt.xlabel("Website")
    plt.ylabel("Content Type (HTTP-Only, HTTPS-Only, Both, or Neither)")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/protocol_significance.png", dpi=300)
    plt.close()

def num_dnsmpi_links():
    results = RESULTS

    websites = results.index.to_list()
    dnsmpi_content = results["Contains DNSMPI-associated Content?"].to_list()

    categories = ["Has DNSMPI content", "Does not have DNSMPI content"]
    dnsmpi = dnsmpi_content.count("Yes")
    no_dnsmpi = dnsmpi_content.count("No")
    data = [dnsmpi, no_dnsmpi]

    plt.figure(figsize=(20, 8))
    plt.bar(categories, data, color=['olivedrab', 'firebrick'])
    plt.title("DNSMPI Content")
    plt.xlabel("Has Content")
    plt.ylabel("Number of Websites")
    plt.xticks(ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/number_of_dnsmpi_links.png", dpi=300)
    plt.close()

def percent_websites_per_category_with_dnsmpi_links():
    results = RESULTS

    websites = results.index.to_list()
    dnsmpi_content = results["Contains DNSMPI-associated Content?"].to_list()

    percent_dnsmpi = []

    categories = ["Luxury Clothing Brands", "Fast Fashion Clothing Brands", "Technology Brands", "Vehicle Brands"]
    
    sites_by_category ={
        "luxury_clothing_sites" : websites[:25],
        "fast_fashion_sites" : websites[25:50],
        "tech_sites" : websites[50:75],
        "vehicle_sites" : websites[75:]
    }

    for cat in sites_by_category:
        num_dnsmpi = 0
        tot = 25
        for site in sites_by_category.get(cat):
            dnsmpi_content = results.loc[site, "Contains DNSMPI-associated Content?"]
            if dnsmpi_content == "Yes":
                num_dnsmpi +=1

        percent = (num_dnsmpi / tot) * 100
        percent_dnsmpi.append(percent)

    fig, ax = plt.subplots()
    ax.pie(percent_dnsmpi, labels=categories, autopct='%1.3f%%', colors =["lightgreen","orchid","slateblue","goldenrod"])
    plt.title("Percent Websites with DNSMPI Links by Category")
    plt.ylabel("")
    plt.xlabel("")
    plt.savefig("analysis/ImageFiles/percent_by_cat_w_dnsmpi.png", dpi=300)
    plt.close()

def cookies_to_dnsmpi_links():
    results = RESULTS

    websites = results.index.to_list()
    dnsmpi_content = results["Contains DNSMPI-associated Content?"].to_list()
    num_cookies = results["Number of Cookies"].to_list()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x=dnsmpi_content, y=num_cookies, palette="Set2")

    plt.title('Cookie Number by DNSMPI Status')
    plt.xlabel('DNSMPI Status')
    plt.ylabel('Number of Cookies')
    plt.savefig("analysis/ImageFiles/cookies_by_dnsmpi_links.png", dpi=300)
    plt.close()

def cookies_with_http_only_tf():
    results = RESULTS

    websites = results.index.to_list()
    cookie_analysis = {}

    for site in websites:
        cookie_string = results.loc[site, "Cookie Information"]
        site_cookies = ast.literal_eval(cookie_string)
            
        cookie_details = site_cookies[1:]
            
        total_cookies = int(site_cookies[0].split(':')[1].strip())
        num_true = len([cookie for cookie in cookie_details if cookie.get('HttpOnly', False) is True])
        num_false = len([cookie for cookie in cookie_details if cookie.get('HttpOnly', False) is False])

        cookie_analysis[site] = [total_cookies, num_true, num_false]

    sites = list(cookie_analysis.keys())
    totals = [cookie_analysis[site][0] for site in sites]
    true_cookies = [cookie_analysis[site][1] for site in sites]
    false_cookies = [cookie_analysis[site][2] for site in sites]

    x = np.arange(len(sites))  # the label locations
    width = 0.6  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, true_cookies, width, label='HttpOnly: True', color='slateblue')
    ax.bar(x, false_cookies, width, bottom=true_cookies, label='HttpOnly: False', color='palevioletred')
    ax.legend(title="HttpOnly", fontsize=8)
    plt.title("Number of Pages per Website")
    plt.xlabel("Website")
    plt.ylabel("Number of Pages")
    plt.xticks(ticks=range(len(COMPANY_NAMES)), labels=COMPANY_NAMES, rotation=90, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/number_of_cookies_with_http_only.png", dpi=300)
    plt.close()

def get_cookie_details():
    results = RESULTS
    websites = results.index.to_list()

    cookie_name_counts = {}
    cookie_names = []

    num_cookies_exp = {}

    cookie_domain_counts = {}
    cookie_domains = []
    cookie_name_to_domain = {}

    num_secure_cookies = {}
    num_http_only = {}

    cookie_safety = {}

    sites_with_cookie = {}

    for site in websites:
        cookie_string = results.loc[site, "Cookie Information"]
        site_cookies = ast.literal_eval(cookie_string)
            
        cookie_details = site_cookies[1:]
            
        total_cookies = int(site_cookies[0].split(':')[1].strip())

        num_cookies_expire = 0
        num_cookies_no_expire = 0

        num_cookies_secure = 0
        num_cookies_not_secure = 0

        num_true = 0
        num_false = 0

        for cookie in cookie_details:
            name = cookie.get("Name")
            expiration = cookie.get("Expires")
            secure = cookie.get("Secure")
            domain = cookie.get("Domain")
            http = cookie.get('HttpOnly')

            safety = []

            cookie_name_counts[name] = cookie_name_counts.get(name, 0) + 1
            cookie_names.append(name)

            if expiration != -1:
                num_cookies_expire += 1
                safety.append(f"Expires at {expiration}")
            elif expiration == -1:
                num_cookies_no_expire += 1
                safety.append(f"Does not expire")
            
            cookie_domain_counts[domain] = cookie_domain_counts.get(domain, 0) + 1
            cookie_domains.append(domain)

            if name not in cookie_name_to_domain:
                cookie_name_to_domain[name] = []
            cookie_name_to_domain[name].append(domain)

            if secure is True:
                num_cookies_secure += 1
                safety.append("Secure")
            elif secure is False:
                num_cookies_not_secure += 1
                safety.append("Not secure")

            if http is True:
                num_true += 1
                safety.append("HTTP Only")
            elif http is False:
                num_false += 1
                safety.append("Not HTTP Only")

            cookie_safety[name] = safety

            if name not in sites_with_cookie:
                sites_with_cookie[name] = []
            sites_with_cookie[name].append(site)

        num_cookies_exp[site] = [num_cookies_expire, num_cookies_no_expire, total_cookies]
        num_secure_cookies[site] = [num_cookies_secure, num_cookies_not_secure, total_cookies]
        num_http_only[site] = [num_true, num_false, total_cookies]

    unique_cookie_names = list(set(cookie_names))
    unique_cookie_domains = list(set(cookie_domains))

    return unique_cookie_names, cookie_name_counts, num_cookies_exp, unique_cookie_domains, cookie_domain_counts, num_secure_cookies, num_http_only, cookie_name_to_domain, cookie_safety, sites_with_cookie


def cookies_all_websites():
    results = RESULTS

    websites = results.index.to_list()
    details = get_cookie_details()

    names = details[0]
    name_counts = details[1]
    counts = [name_counts[name] for name in names]

    # Filter cookies that appear more than once
    filtered_names = [name for name in names if name_counts[name] > 1]
    filtered_counts = [name_counts[name] for name in filtered_names]

    plt.figure(figsize=(20, 8))
    plt.bar(filtered_names, filtered_counts, color='mediumpurple')
    plt.title("Cookies Which Appear Across 2+ Websites")
    plt.xlabel("Cookie Names")
    plt.ylabel("Number of Cookies")
    plt.xticks(rotation=90, ha='center', fontsize=6)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/all_site_cookies.png", dpi=300)
    plt.close()

def cookie_domains_all_websites():
    results = RESULTS

    websites = results.index.to_list()
    details = get_cookie_details()

    domains = details[3]
    domain_counts = details[4]
    counts = [domain_counts[domain] for domain in domains]

    # Filter cookies that appear more than once
    filtered_domains = [domain for domain in domains if domain_counts[domain] > 1]
    filtered_counts = [domain_counts[domain] for domain in filtered_domains]

    plt.figure(figsize=(20, 8))
    plt.bar(filtered_domains, filtered_counts, color='darkorchid')
    plt.title("Domains for Cookies Which Appear Across 2+ Websites")
    plt.xlabel("Domain Names")
    plt.ylabel("Number of Cookies at Domain")
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig("analysis/ImageFiles/all_site_cookie_domains.png", dpi=300)
    plt.close()

def percent_secure_cookies_by_category():
    results = RESULTS

    websites = results.index.to_list()
    cookie_details = get_cookie_details()

    secure = cookie_details[5]
    percent_secure = []

    categories = ["Luxury Clothing Brands", "Fast Fashion Clothing Brands", "Technology Brands", "Vehicle Brands"]
    
    sites_by_category ={
        "luxury_clothing_sites" : websites[:25],
        "fast_fashion_sites" : websites[25:50],
        "tech_sites" : websites[50:75],
        "vehicle_sites" : websites[75:]
    }

    for cat in sites_by_category:
        num_secure = 0
        tot = 0
        for site in sites_by_category.get(cat):
            site_info = secure[site]
            num_secure += site_info[0]
            tot += site_info[2]

        if tot !=0:
            percent = (num_secure / tot) * 100
        elif tot == 0 or tot is None:
            percent = 0  # Assign 0% if no data available
        percent_secure.append(percent)

    fig, ax = plt.subplots()
    ax.pie(percent_secure, labels=categories, autopct='%1.3f%%', colors =["lightgreen","orchid","slateblue","goldenrod"])
    plt.title("Percent Secure Cookies by Category")
    plt.ylabel("")
    plt.xlabel("")
    plt.savefig("analysis/ImageFiles/percent_secure_cookies_by_cat.png", dpi=300)
    plt.close()

def percent_http_only_cookies_by_category():
    results = RESULTS

    websites = results.index.to_list()
    cookie_details = get_cookie_details()

    http = cookie_details[6]
    percent_http = []

    categories = ["Luxury Clothing Brands", "Fast Fashion Clothing Brands", "Technology Brands", "Vehicle Brands"]
    
    sites_by_category ={
        "luxury_clothing_sites" : websites[:25],
        "fast_fashion_sites" : websites[25:50],
        "tech_sites" : websites[50:75],
        "vehicle_sites" : websites[75:]
    }

    for cat in sites_by_category:
        num_http = 0
        tot = 0
        for site in sites_by_category.get(cat):
            site_info = http[site]
            num_http += site_info[0]
            tot += site_info[2]

        if tot == 0:
            percent = 0
        else:
            percent = (num_http / tot) * 100
        percent_http.append(percent)

    fig, ax = plt.subplots()
    ax.pie(percent_http, labels=categories, autopct='%1.3f%%', colors =["lightgreen","orchid","slateblue","goldenrod"])
    plt.title("Percent HTTP Only Cookies by Category")
    plt.ylabel("")
    plt.xlabel("")
    plt.savefig("analysis/ImageFiles/percent_http_only_cookies_by_cat.png", dpi=300)
    plt.close()

def percent_cookies_that_do_not_expire_by_category():
    results = RESULTS

    websites = results.index.to_list()
    cookie_details = get_cookie_details()

    exp = cookie_details[2]
    percent_no_exp = []

    categories = ["Luxury Clothing Brands", "Fast Fashion Clothing Brands", "Technology Brands", "Vehicle Brands"]
    
    sites_by_category ={
        "luxury_clothing_sites" : websites[:25],
        "fast_fashion_sites" : websites[25:50],
        "tech_sites" : websites[50:75],
        "vehicle_sites" : websites[75:]
    }

    for cat in sites_by_category:
        num_no_exp = 0
        tot = 0
        for site in sites_by_category.get(cat):
            site_info = exp[site]
            num_no_exp += site_info[0]
            tot += site_info[2]

        percent = (num_no_exp / tot) * 100
        percent_no_exp.append(percent)

    fig, ax = plt.subplots()
    ax.pie(percent_no_exp, labels=categories, autopct='%1.3f%%', colors =["lightgreen","orchid","slateblue","goldenrod"])
    plt.title("Percent Cookies That Don't Expire by Category")
    plt.ylabel("")
    plt.xlabel("")
    plt.savefig("analysis/ImageFiles/percent_cookies_that_do_not_expire_by_cat.png", dpi=300)
    plt.close()

def cookie_datatable():
    results = RESULTS
    websites = results.index.to_list()
    cookie_details = get_cookie_details()
    df_info = {}

    col_names = ["Cookie Name","Domains Associated With", "Cookie Expiration", "Cookie Security", "HTTP Only Status", "Total Number of Sites With Cookie", 
    "Number of Luxury Clothing Companies With Cookie", "Number of Fast Fashion Companies With Cookie", "Number of Technology Companies With Cookie", 
    "Number of Car Companies with Cookie"]

    # col_names = ["Cookie Name","Domains Associated With", "Cookie Expiration", "Cookie Security", "HTTP Only Status", "Total Number of Sites With Cookie"] 

    cookie_names = cookie_details[0]

    num_cookies = cookie_details[1]
    name_to_domain = cookie_details[7]
    cookie_safety = cookie_details[8]

    sites_with_cookie = cookie_details[9]

    rows = []  # Collect rows of data

    for name in cookie_names:
        info_list = [name]

        associated_domains = name_to_domain.get(name)
        info_list.append(associated_domains)

        safety_features = cookie_safety.get(name)
        for safety_feature in safety_features:
            info_list.append(safety_feature)

        appears_on = num_cookies.get(name)
        info_list.append(appears_on)

        category_appearances = calc_num_appearances_by_cat(name, websites, sites_with_cookie)
        info_list.append(category_appearances[0])
        info_list.append(category_appearances[1])
        info_list.append(category_appearances[2])
        info_list.append(category_appearances[3])

        rows.append(info_list)  # Append the row of info

    df = pd.DataFrame(rows, columns=col_names)
    df.to_csv("analysis/cookie_summary_data.csv")


def calc_num_appearances_by_cat(cookie_name, websites, sites_with_cookie):
    sites_by_category = {
        "luxury_clothing_sites" : websites[:25],
        "fast_fashion_sites" : websites[25:50],
        "tech_sites" : websites[50:75],
        "vehicle_sites" : websites[75:]
    }

    appears_on = []
    
    for category, websites in sites_by_category.items():
        current_sites = sites_with_cookie.get(cookie_name)
        count = 0
        for site in current_sites:
            if site in websites:
                count+=1
        cat_count = count
        appears_on.append(cat_count)
    
    return appears_on

def summary_statistics():
    results = RESULTS
    summary_stats = results.describe()
    summary_stats.to_csv("analysis/summary_statistics.csv")

def correlation_matrix(column1, column2):
    results = RESULTS
    corr_matrix = results[[column1, column2]].corr()

def main():
    # pages_per_website()
    # cookies_per_website()
    # avg_pages_cookies_by_category()
    # pages_cookies_by_category()
    # page_cookie_correlation()
    mixed_content()
    # num_dnsmpi_links()
    # percent_websites_per_category_with_dnsmpi_links()

    # cookies_with_http_only_tf()
    cookies_all_websites()
    cookies_to_dnsmpi_links()
    cookie_domains_all_websites()
    percent_secure_cookies_by_category()
    percent_http_only_cookies_by_category()
    percent_cookies_that_do_not_expire_by_category()
    percent_websites_per_category_with_dnsmpi_links()
    #protocol_content()
    

    summary_statistics()
    cookie_datatable()

if __name__ == "__main__":
    main()