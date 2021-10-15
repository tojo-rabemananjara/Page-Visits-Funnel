import pandas as pd

#initializing dataframes
visits = pd.read_csv('visits.csv',
                     parse_dates=[1])
cart = pd.read_csv('cart.csv',
                   parse_dates=[1])
checkout = pd.read_csv('checkout.csv',
                       parse_dates=[1])
purchase = pd.read_csv('purchase.csv',
                       parse_dates=[1])

#displaying dataframe heads
print(visits.head())
print(cart.head())
print(checkout.head())
print(purchase.head())

#show percent loss from visit to cart
cart_visit_len = len(pd.merge(visits, cart, how='left'))
num_cart_null = len(cart.cart_time.isnull())
print("percent loss from visit to cart {}%".format(num_cart_null/float(cart_visit_len)*100))

#show percent loss from cart to checkout
cart_checkout_len = len(pd.merge(cart, checkout, how='left'))
num_checout_null = len(checkout.checkout_time.isnull())
print("percent loss from cart to checkout {}%".format(num_checout_null/float(cart_checkout_len)*100))

#left merge chain to get percent loss overall
all_data = visits.merge(cart, how='left').merge(checkout, how='left').merge(checkout, how='left').merge(purchase, how='left')

#show percent loss from checkout to purchase
checkout_purchase_funnel = all_data[(~all_data.checkout_time.isnull()) & (all_data.purchase_time.isnull())]
print("percent loss from cart to checkout {}%".format(len(checkout_purchase_funnel)/float(len(all_data))*100))


all_data['time_to_purchase'] = \
    all_data.purchase_time - \
    all_data.visit_time

#print(all_data.time_to_purchase)
#show mean time to purchase an item
print(all_data.time_to_purchase.mean())

#Looking at these percent losses, most attention needs to brought to the cart-checkout chain as
# it has the highest percent loss (74.68)
