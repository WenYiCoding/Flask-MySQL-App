import requests

BASE_URL = 'http://127.0.0.1:5000/api'

def display_menu():
    print("\n" + "="*35)
    print("  INTERNSHIP APPLICATION TRACKER  ")
    print("="*35)
    print("1. View All Applications")
    print("2. Add New Application")
    print("3. Update Application Status")
    print("4. Delete Application Entry")
    print("5. Exit")
    print("="*35)

def view_applications():
    try:
        response = requests.get(f"{BASE_URL}/applications")
        result = response.json()

        if result.get('status') == 'success':
            apps = result.get('data') or result.get("message")

            if not apps:
                print("\n[!] No applications found yet.")
                return
            
            print(f"\n{'ID':<5} | {'Company':<20} | {'Job Title':<25} | {'Status':<15}")
            print("-" * 75)

            for app in apps:
                print(f"{app['id']:<5} | {app['company_name']:<20} | {app['job_title']:<25} | {app['apply_status']:<15}")

        else:
            print("[!] Error from server:", result.get("message"))

    except Exception as e:
        print("[!] Could not connect to backend server.", e)

def add_application():
    print("\n--- Add New Record ---")
    company = input("Enter Company Name: ")
    job = input("Enter Job Title: ")
    
    if not company or not job:
        print("[!] Fields cannot be empty.")
        return
        
    payload = {
        "company_name": company,
        "job_title": job
    }
    
    try:
        # Trigger your Flask POST route
        response = requests.post(f"{BASE_URL}/add-application", json=payload)
        result = response.json()
        print(f"\n[+] Server Response: {result.get('message')}")
    except Exception as e:
        print("[!] Operation failed.", e)

def update_status():
    print("\n--- Update Application Status ---")
    app_id = input("Enter Application ID to update: ")
    new_status = input("Enter New Status (e.g., Interviewing, Offered, Rejected): ")
    
    if not app_id or not new_status:
        print("[!] Fields cannot be empty.")
        return
        
    payload = {
        "id": int(app_id),
        "status": new_status
    }
    
    try:
        # Trigger your Flask PUT route
        response = requests.put(f"{BASE_URL}/update-status", json=payload)
        result = response.json()
        print(f"\n[+] Server Response: {result.get('message')}")
    except Exception as e:
        print("[!] Operation failed.", e)

def delete_application():
    print("\n--- Delete Application Entry ---")
    app_id = input("Enter Application ID to delete: ")
    
    if not app_id:
        print("[!] Field cannot be empty.")
        return
        
    payload = {
        "id": int(app_id)
    }
    
    try:
        # Trigger your Flask DELETE route
        response = requests.delete(f"{BASE_URL}/delete-application", json=payload)
        result = response.json()
        print(f"\n[+] Server Response: {result.get('message')}")
    except Exception as e:
        print("[!] Operation failed.", e)

def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            view_applications()
        elif choice == "2":
            add_application()
        elif choice == "3":
            update_status()
        elif choice == "4":
            delete_application()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("[!] Invalid option. Try again.")

if __name__ == "__main__":
    main()