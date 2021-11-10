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

#dropping duplicate ids because they shouldn't be counted in percent losses
visits = visits.drop_duplicates(subset='user_id').reset_index(drop=True)
cart = cart.drop_duplicates(subset='user_id').reset_index(drop=True)
checkout = checkout.drop_duplicates(subset='user_id').reset_index(drop=True)
purchase = purchase.drop_duplicates(subset='user_id').reset_index(drop=True)
# print(visits)

#NOTE!
#multiple users with the same ID appear more than once in the 
# cart list and confirmed this is due to multiple users visiting
# the cart page more than once within the same visit.

#displaying dataframe heads
# print(visits.head())
# print(cart.head())
# print(checkout.head())
# print(purchase.head())

# print(visits.describe())
# print(cart.describe())
# print(checkout.describe())
# print(purchase.describe())

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
mean_time_to_purchase = all_data.time_to_purchase.mean()
print('mean time to purchase: {}'.format(mean_time_to_purchase))

#Looking at these percent losses, most attention needs to brought tco the visit-cart chain since
# it has the highest percent loss (82.56%) out of the 3 parts of the chain.

#extra testing to check that the 2 methods of percent loss calculations (here and above) agree
# visit_cart = all_data[(~all_data.visit_time.isnull()) & (all_data.cart_time.isnull())]
# print(len(visit_cart)/float(len(visits))*100)
# cart_checkout = all_data[(~all_data.cart_time.isnull()) & (all_data.checkout_time.isnull())]
# print(len(cart_checkout)/float(len(cart))*100)
# checkout_purchase = all_data[(~all_data.checkout_time.isnull()) & (all_data.purchase_time.isnull())]
# print(len(checkout_purchase)/float(len(checkout))*100)
