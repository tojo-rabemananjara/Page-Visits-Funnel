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

#dropping duplicate ids because they shouldn't be counted
visits = visits.drop_duplicates(subset='user_id')
cart = cart.drop_duplicates(subset='user_id')
checkout = checkout.drop_duplicates(subset='user_id')
purchase = purchase.drop_duplicates(subset='user_id')


#displaying dataframe heads
# print(visits.head())
# print(cart.head())
# print(checkout.head())
# print(purchase.head())

print(visits.describe())
print(cart.describe())
print(checkout.describe())
print(purchase.describe())

#show percent loss from visit to cart
visit_cart = pd.merge(visits, cart, how='left')
cart_null = visit_cart[(~visit_cart.visit_time.isnull()) & (visit_cart.cart_time.isnull())]
print("percent loss from visit to cart {}%".format(len(cart_null)/float(len(visit_cart))*100))

#show percent loss from cart to checkout
cart_checkout = pd.merge(cart, checkout, how='left')
checkout_null = cart_checkout[(~cart_checkout.cart_time.isnull()) & (cart_checkout.checkout_time.isnull())]
print("percent loss from cart to checkout {}%".format(len(checkout_null)/float(len(cart_checkout))*100))

#show percent loss from checkout to purchase
checkout_purchase = pd.merge(checkout, purchase, how='left')
purchase_null = checkout_purchase[(~checkout_purchase.checkout_time.isnull()) & (checkout_purchase.purchase_time.isnull())]
print("percent loss from checkout to purchase {}%".format(len(purchase_null)/float(len(checkout_purchase))*100))

#left merge chain to get percent loss overall
all_data = visits.merge(cart, how='left').merge(checkout, how='left').merge(purchase, how='left')

all_data['time_to_purchase'] = \
    all_data.purchase_time - \
    all_data.visit_time

#print(all_data.info())
#show mean time to purchase an item
print(all_data.time_to_purchase.mean())

#Looking at these percent losses, most attention needs to brought tco the cart-checkout chain as
# it has the highest percent loss (74.68)

#extra testing to check that the 2 things agree
visit_cart = all_data[(~all_data.visit_time.isnull()) & (all_data.cart_time.isnull())]
print(len(visit_cart)/float(len(visits))*100)
cart_checkout = all_data[(~all_data.cart_time.isnull()) & (all_data.checkout_time.isnull())]
print(len(cart_checkout)/float(len(cart))*100)
checkout_purchase = all_data[(~all_data.checkout_time.isnull()) & (all_data.purchase_time.isnull())]
print(len(checkout_purchase)/float(len(checkout))*100)