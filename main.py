import os
import pandas as pd
from src.DBInteractor import DBInteractor
import logging
from src.read_dbinfo_yaml import read_dbinfo_yaml
from src.visualizations import make_bar_chart, make_bubble_chart, make_double_line_plot

# Set up logger
logging.basicConfig(
    level=logging.DEBUG,
    filename="output.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)

# Read database info from yaml
dbinfo = read_dbinfo_yaml("dbinfo.yaml")

# Connect to database
db_interactor = DBInteractor(dbinfo)
db_interactor.connect_db()

# Get data from database
coupon_data = db_interactor.pull_channel_promotion_data()
coupon_seasonal_data = db_interactor.pull_timeseries_data()

# Group dataframe for visualizations
# Group by channel
channel_grouped = coupon_data.groupby("channel", as_index=False).agg("sum")[
    ["channel", "count_total", "coupon_true", "purchase_true"]
]
channel_grouped["PurchasePercentage"] = (
    100 * channel_grouped["purchase_true"] / channel_grouped["count_total"]
)
channel_grouped["PurchasePercentage"] = channel_grouped["PurchasePercentage"].round(2)
channel_grouped["CouponUsePercentage"] = (
    100 * channel_grouped["coupon_true"] / channel_grouped["count_total"]
)
channel_grouped["CouponUsePercentage"] = channel_grouped["CouponUsePercentage"].round(2)

# Group by promotion type
promotion_grouped = coupon_data.groupby("promotion_type", as_index=False).agg("sum")[
    ["promotion_type", "count_total", "coupon_true", "purchase_true"]
]
promotion_grouped["PurchasePercentage"] = (
    100 * promotion_grouped["purchase_true"] / promotion_grouped["count_total"]
)
promotion_grouped["PurchasePercentage"] = promotion_grouped["PurchasePercentage"].round(
    2
)
promotion_grouped["CouponUsePercentage"] = (
    100 * promotion_grouped["coupon_true"] / promotion_grouped["count_total"]
)
promotion_grouped["CouponUsePercentage"] = promotion_grouped[
    "CouponUsePercentage"
].round(2)

# Visualizations
logging.info('Making visualizations...')
# Create directory if it doesn't exist
if not os.path.exists("images"):
    os.mkdir("images")

# Coupon as a Brand Reminder
fig = make_bubble_chart(
    data_frame=coupon_data,
    x="promotion_type",
    y="channel",
    size="percent_purchase_true",
    color="percent_purchase_true",
    xlabel="Promotion Type",
    ylabel="Promotion Channel",
    title="Coupon Effectiveness as Brand Reminder",
    ctitle="Purchase Percentage",
    savepath="images/purchase_vs_channel_and_type.pdf",
)

# Purchase Percentage vs Channel
fig = make_bar_chart(
    data_frame=channel_grouped,
    x="channel",
    y="PurchasePercentage",
    xlabel="Promotion Channel",
    ylabel="Purchase Percentage",
    savepath="images/purchase_vs_channel.pdf",
)

# Purchase Percentage vs Promotion
fig = make_bar_chart(
    data_frame=promotion_grouped,
    x="promotion_type",
    y="PurchasePercentage",
    xlabel="Promotion Type",
    ylabel="Purchase Percentage",
    savepath="images/purchase_vs_type.pdf",
)

# Coupon Attractiveness
fig = make_bubble_chart(
    data_frame=coupon_data,
    x="promotion_type",
    y="channel",
    size="percent_coupon_true",
    color="percent_coupon_true",
    xlabel="Promotion Type",
    ylabel="Promotion Channel",
    title="Coupon Attractiveness",
    ctitle="Coupon Use Percentage",
    savepath="images/coupon_use_vs_channel_and_type.pdf",
)

# Purchase Percentage vs Channel
fig = make_bar_chart(
    data_frame=channel_grouped,
    x="channel",
    y="CouponUsePercentage",
    xlabel="Promotion Channel",
    ylabel="Coupon Use Percentage",
    savepath="images/coupon_use_vs_channel.pdf",
)

# Purchase Percentage vs Promotion
fig = make_bar_chart(
    data_frame=promotion_grouped,
    x="promotion_type",
    y="CouponUsePercentage",
    xlabel="Promotion Type",
    ylabel="Coupon Use Percentage",
    savepath="images/coupon_use_vs_type.pdf",
)

# Seasonality Effects
coupon_seasonal_data = coupon_seasonal_data.groupby("week_number", as_index=False).agg(
    "mean"
)
fig = make_double_line_plot(
    data_frame=coupon_seasonal_data,
    x="week_number",
    y0="percent_coupon_true",
    y1="percent_purchase_true",
    ylabel0="Purchase Percentage",
    ylabel1="Coupon Use Percentage",
    xlabel="Week Number",
    title="Seasonal User Purchase Patterns",
    savepath="images/purchase_and_coupon_use_seasonality.pdf",
)
