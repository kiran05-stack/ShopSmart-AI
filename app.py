import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ShopSmart AI",
    page_icon="🛍️",
    layout="wide"
)

# PAGE HEADER
st.title("🛍️ ShopSmart AI")
st.subheader("Your AI Business Assistant for Small Shops")

st.write(
    "Understand sales, discover opportunities, "
    "and make smarter business decisions."
)

st.divider()

# SIDEBAR SETTINGS
st.sidebar.title("🏪 Shop Settings")

shop_name = st.sidebar.text_input(
    "Shop name",
    value="My Grocery Store"
)

owner_name = st.sidebar.text_input(
    "Owner name",
    value="Shop Owner"
)

st.sidebar.header("Today's Business Data")

sales = st.sidebar.number_input(
    "Today's sales (₹)",
    min_value=0.0,
    value=5000.0,
    step=500.0
)

expenses = st.sidebar.number_input(
    "Today's expenses (₹)",
    min_value=0.0,
    value=3000.0,
    step=100.0
)

customers = st.sidebar.number_input(
    "Number of customers",
    min_value=0,
    value=50,
    step=1
)

# CALCULATIONS
profit = sales - expenses

average_sale = sales / customers if customers > 0 else 0

profit_margin = (
    (profit / sales) * 100
    if sales > 0
    else 0
)

# DASHBOARD
st.header(f"Welcome, {owner_name}!")
st.caption(f"Business: {shop_name}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Today's Revenue", f"₹{sales:,.2f}")
col2.metric("Expenses", f"₹{expenses:,.2f}")
col3.metric("Profit / Loss", f"₹{profit:,.2f}")
col4.metric("Customers", f"{customers:,}")

st.divider()

# BUSINESS CHART
st.header("📊 Business Performance")

chart_data = pd.DataFrame({
    "Category": ["Revenue", "Expenses", "Profit / Loss"],
    "Amount": [sales, expenses, profit]
})

fig = px.bar(
    chart_data,
    x="Category",
    y="Amount",
    color="Category",
    title="Today's Financial Overview",
    text="Amount"
)

fig.update_layout(
    showlegend=False,
    xaxis_title="",
    yaxis_title="Amount (₹)"
)

st.plotly_chart(fig, use_container_width=True)

st.metric("Profit Margin", f"{profit_margin:.1f}%")

st.divider()

# PRODUCT SALES TRACKER
st.header("🛒 Product Sales Tracker")

st.write(
    "Enter the products sold today to identify "
    "your best-selling products."
)

if "products" not in st.session_state:
    st.session_state.products = pd.DataFrame({
        "Product": ["Milk", "Bread", "Biscuits"],
        "Units Sold": [30, 20, 10],
        "Price Per Unit (₹)": [30.0, 40.0, 20.0]
    })

edited_products = st.data_editor(
    st.session_state.products,
    num_rows="dynamic",
    use_container_width=True,
    key="product_editor"
)

if not edited_products.empty:

    edited_products["Units Sold"] = pd.to_numeric(
        edited_products["Units Sold"],
        errors="coerce"
    ).fillna(0)

    edited_products["Price Per Unit (₹)"] = pd.to_numeric(
        edited_products["Price Per Unit (₹)"],
        errors="coerce"
    ).fillna(0)

    edited_products["Product Revenue (₹)"] = (
        edited_products["Units Sold"]
        * edited_products["Price Per Unit (₹)"]
    )

    st.dataframe(
        edited_products,
        use_container_width=True,
        hide_index=True
    )

    valid_products = edited_products[
        edited_products["Product"].astype(str).str.strip() != ""
    ]

    if not valid_products.empty:

        best_product = valid_products.loc[
            valid_products["Units Sold"].idxmax()
        ]

        st.info(
            f"🏆 Best-selling product: {best_product['Product']} "
            f"({best_product['Units Sold']:.0f} units)"
        )

st.divider()

# BUSINESS ADVISOR
st.header("🤖 ShopSmart Business Advisor")

st.write(
    "Get business suggestions based on the numbers "
    "you enter."
)

if sales == 0 and expenses == 0:

    st.info(
        "Enter your sales and expenses to receive "
        "business suggestions."
    )

elif profit < 0:

    st.warning(
        "Your expenses are higher than your sales. "
        "Review your costs and check whether you can "
        "reduce unnecessary spending."
    )

elif profit == 0:

    st.info(
        "Your business has broken even today. "
        "Look for ways to increase sales or reduce costs."
    )

else:

    st.success(
        f"Your business made ₹{profit:,.2f} "
        "before other unrecorded costs or taxes."
    )

    if profit_margin < 10:

        st.write(
            "Suggestion: Review product costs, pricing, "
            "and operating expenses to identify ways "
            "to improve your profit margin."
        )

    else:

        st.write(
            "Suggestion: Track profitable products "
            "and maintain appropriate stock levels."
        )

if customers > 0:

    st.write(
        f"💡 Average revenue per customer: ₹{average_sale:,.2f}"
    )

    st.write(
        "Consider relevant product bundles or promotions "
        "to encourage customers to buy complementary items."
    )

else:

    st.info(
        "Enter your customer count to calculate "
        "average revenue per customer."
    )

st.divider()

# MARKETING MESSAGE GENERATOR
st.header("📣 Marketing Message Generator")

product_name = st.text_input(
    "Product to promote",
    value="Fresh Milk"
)

offer = st.text_input(
    "Offer or discount",
    value="Special offer today"
)

if st.button("Generate Promotional Message"):

    if product_name.strip() and offer.strip():

        message = (
            f"Hello customers! 🛍️ Visit {shop_name} "
            f"today for {product_name}. "
            f"{offer}! We look forward to serving you. 😊"
        )

        st.success("Your promotional message is ready!")

        st.code(message, language=None)

        st.caption(
            "This is a template-based message generator. "
            "It does not yet use an external AI model."
        )

    else:

        st.error(
            "Please enter both a product name and an offer."
        )

st.divider()

# FOOTER
st.caption(
    "ShopSmart AI | Hackathon Prototype | "
    "Business insights are estimates based on the data entered."
)

st.caption(
    "This prototype uses calculations and predefined rules. "
    "It does not yet connect to a live AI model or Paytm systems."
)