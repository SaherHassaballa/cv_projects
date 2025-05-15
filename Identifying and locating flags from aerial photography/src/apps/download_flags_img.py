import os
import requests
import pycountry

# مجلد حفظ الأعلام
output_folder = r"c:\Users\saher\Desktop\github\cv_projects\Identifying and locating flags from aerial photography\src\data\downloaded_countury_flags"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# الدول اللي عندك بالفعل
# existing_countries = {  # beacase i have this flags so i wont download them agin
#     "italy", "argentina", "india", "qatar", "usa", "uk",
#     "bulgaria", "china", "croatia", "denmark", "egypt", "ghana",
#     "iraq", "iran", "libya", "romania", "spain", "turkey"
# }

# تحميل باقي الأعلام
for country in pycountry.countries:
    country_name = country.name.lower()
    country_code = country.alpha_2.lower()

    # # تخطي الدول اللي عندك
    # if (
    #     country_name in existing_countries or
    #     country.alpha_2.lower() in existing_countries
    # ):
    #     continue

    # تكوين الرابط
    url = f"https://flagcdn.com/w320/{country_code}.png"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            file_path = os.path.join(output_folder, f"{country_name}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved flag: {country_name}")
        else:
            print(f"❌ Failed ({response.status_code}): {country_name}")
    except Exception as e:
        print(f"⚠️ Error downloading {country_name}: {e}")
