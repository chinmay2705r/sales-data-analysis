# Sales Data Analysis — Chinmay Kumar Gupta
# Tools: Python, Pandas, Matplotlib, Seaborn

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── 1. Create sample dataset (mirrors real Superstore data) ──────────────────
np.random.seed(28)
n = 500

categories    = ['Pixel Phone', 'Dress', 'Furniture', 'Groceries', 'Novels']
regions       = ['Delhi', 'TamilNadu', 'Assam', 'Gujrat']
months        = ['January','Febuary','March','April','May','June',
                 'July','August','September','October','November','December']

data = {
    'Order_ID'  : [f'ORD{1000+i}' for i in range(n)],
    'Month'     : np.random.choice(months, n),
    'Category'  : np.random.choice(categories, n),
    'Region'    : np.random.choice(regions, n),
    'Sales'     : np.round(np.random.uniform(50, 2000, n), 2),
    'Profit'    : np.round(np.random.uniform(-100, 500, n), 2),
    'Quantity'  : np.random.randint(1, 10, n),
    'Discount'  : np.round(np.random.uniform(0, 0.5, n), 2),
}
df = pd.DataFrame(data)
df.to_csv('sales_data.csv', index=False)
print("Dataset created:", df.shape)
print(df.head())

# 2. Basic EDA 
print("\n── Summary Stats ──")
print(df[['Sales','Profit','Quantity','Discount']].describe().round(2))

print("\n── Null Values ──")
print(df.isnull().sum())

print("\n── Sales by Category ──")
print(df.groupby('Category')['Sales'].sum().sort_values(ascending=False).round(2))

print("\n── Sales by Region ──")
print(df.groupby('Region')['Sales'].sum().sort_values(ascending=False).round(2))

# ── 3. Visualisations 
sns.set_theme(style='whitegrid', palette='muted')
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Sales Performance Dashboard\nChinmay Kumar Gupta | Data Analytics Project',
             fontsize=14, fontweight='bold', y=1.01)

# Chart 1 — Sales by Category
cat_sales = df.groupby('Category')['Sales'].sum().sort_values()
axes[0,0].barh(cat_sales.index, cat_sales.values,
               color=['#4C72B0','#55A868','#C44E52','#8172B2','#CCB974'])
axes[0,0].set_title('Total Sales by Category', fontweight='bold')
axes[0,0].set_xlabel('Total Sales (₹)')
for i, v in enumerate(cat_sales.values):
    axes[0,0].text(v+10, i, f'₹{v:,.0f}', va='center', fontsize=9)

# Chart 2 — Sales by Region
reg_sales = df.groupby('Region')['Sales'].sum()
colors = ['#4C72B0','#55A868','#C44E52','#8172B2']
axes[0,1].pie(reg_sales.values, labels=reg_sales.index, autopct='%1.1f%%',
              colors=colors, startangle=90)
axes[0,1].set_title('Sales Distribution by Region', fontweight='bold')

# Chart 3 — Monthly Sales Trend
month_order = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
monthly = df.groupby('Month')['Sales'].sum().reindex(month_order)
axes[0,2].plot(monthly.index, monthly.values, marker='o',
               color='#4C72B0', linewidth=2, markersize=6)
axes[0,2].fill_between(range(len(monthly)), monthly.values, alpha=0.15, color='#4C72B0')
axes[0,2].set_title('Monthly Sales Trend', fontweight='bold')
axes[0,2].set_xlabel('Month')
axes[0,2].set_ylabel('Sales (₹)')
axes[0,2].set_xticks(range(len(monthly)))
axes[0,2].set_xticklabels(monthly.index, rotation=45)

# Chart 4 — Profit by Category (box plot)
sns.boxplot(data=df, x='Category', y='Profit', ax=axes[1,0], palette='muted')
axes[1,0].set_title('Profit Distribution by Category', fontweight='bold')
axes[1,0].set_xlabel('Category')
axes[1,0].set_ylabel('Profit (₹)')
axes[1,0].tick_params(axis='x', rotation=15)

# Chart 5 — Sales vs Profit scatter
axes[1,1].scatter(df['Sales'], df['Profit'], alpha=0.4,
                  c=df['Discount'], cmap='coolwarm', s=20)
axes[1,1].set_title('Sales vs Profit (colour = Discount)', fontweight='bold')
axes[1,1].set_xlabel('Sales (₹)')
axes[1,1].set_ylabel('Profit (₹)')
axes[1,1].axhline(0, color='red', linestyle='--', alpha=0.5)
sm = plt.cm.ScalarMappable(cmap='coolwarm',
     norm=plt.Normalize(df['Discount'].min(), df['Discount'].max()))
plt.colorbar(sm, ax=axes[1,1], label='Discount')

# Chart 6 — Top 5 KPIs
axes[1,2].axis('off')
total_sales   = df['Sales'].sum()
total_profit  = df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100
avg_order     = df['Sales'].mean()
top_cat       = df.groupby('Category')['Sales'].sum().idxmax()
top_reg       = df.groupby('Region')['Sales'].sum().idxmax()

kpis = [
    ('Total Sales',     f'₹{total_sales:,.0f}'),
    ('Total Profit',    f'₹{total_profit:,.0f}'),
    ('Profit Margin',   f'{profit_margin:.1f}%'),
    ('Avg Order Value', f'₹{avg_order:,.0f}'),
    ('Top Category',    top_cat),
    ('Top Region',      top_reg),
]
axes[1,2].set_title('Key Performance Indicators', fontweight='bold', pad=10)
for idx, (label, value) in enumerate(kpis):
    y = 0.85 - idx * 0.14
    axes[1,2].text(0.05, y, label + ':', fontsize=11,
                   color='gray', transform=axes[1,2].transAxes)
    axes[1,2].text(0.55, y, value, fontsize=11, fontweight='bold',
                   color='#2c3e50', transform=axes[1,2].transAxes)

plt.tight_layout()
plt.savefig('sales_dashboard.png', dpi=150, bbox_inches='tight')
print("\nDashboard saved as sales_dashboard.png")

#  4. Business Insights 
print("\n── Business Insights ──")
high_discount = df[df['Discount'] > 0.3]
low_profit    = df[df['Profit'] < 0]
print(f"Orders with discount > 30%  : {len(high_discount)} ({len(high_discount)/n*100:.1f}%)")
print(f"Loss-making orders          : {len(low_profit)}  ({len(low_profit)/n*100:.1f}%)")
print(f"Best month by sales         : {monthly.idxmax()} (₹{monthly.max():,.0f})")
print(f"Worst month by sales        : {monthly.idxmin()} (₹{monthly.min():,.0f})")
