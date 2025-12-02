import requests

API_BASE = 'http://127.0.0.1:8000'

def test_api():
    print("🧪 Testing API Endpoints...\n")
    
    # Test 1: Get all freelancers
    print("1️⃣ Testing GET /api/freelancers")
    response = requests.get(f'{API_BASE}/api/freelancers')
    print(f"Status: {response.status_code}")
    if response.ok:
        freelancers = response.json()
        print(f"Found {len(freelancers)} freelancers")
        if freelancers:
            freelancer_id = freelancers[0]['id']
            print(f"First freelancer ID: {freelancer_id}\n")
            
            # Test 2: Get freelancer ratings
            print(f"2️⃣ Testing GET /api/freelancers/{freelancer_id}/ratings")
            ratings_response = requests.get(f'{API_BASE}/api/freelancers/{freelancer_id}/ratings')
            print(f"Status: {ratings_response.status_code}")
            
            if ratings_response.ok:
                ratings_data = ratings_response.json()
                print(f"Rating info: {ratings_data['rating_info']}")
                print(f"Number of reviews: {len(ratings_data['reviews'])}")
                
                if ratings_data['reviews']:
                    print("\n📝 Sample review:")
                    review = ratings_data['reviews'][0]
                    print(f"  - Evaluator: {review.get('evaluator_name', 'N/A')}")
                    print(f"  - Company: {review.get('evaluator_company', 'N/A')}")
                    print(f"  - Rating: {review.get('rating', 'N/A')}")
                    print(f"  - Review: {review.get('review_text', 'N/A')[:50]}...")
                else:
                    print("⚠️ No reviews found")
            else:
                print(f"❌ Error: {ratings_response.text}")
    else:
        print(f"❌ Error: {response.text}")
    
    print("\n3️⃣ Testing GET /api/evaluators")
    evaluators_response = requests.get(f'{API_BASE}/api/evaluators')
    print(f"Status: {evaluators_response.status_code}")
    if evaluators_response.ok:
        evaluators = evaluators_response.json()
        print(f"Found {len(evaluators)} evaluators")
        if evaluators:
            print(f"First evaluator: {evaluators[0]['name']}")

if __name__ == '__main__':
    test_api()