import tkinter as tk
from tkinter import messagebox
import requests
from googletrans import Translator  # Google Translate API 사용

class RecipeRecommendation:
    def __init__(self, parent, fridge, freezer, room_temp, api_key):
        self.api_key = api_key
        self.fridge = fridge
        self.freezer = freezer
        self.room_temp = room_temp
        self.translator = Translator()  # 번역기 초기화

        # 프레임 생성 및 UI 설정
        self.frame = tk.Frame(parent, bg="#E3F2FD")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_ui()

    def create_ui(self):
        # 요리 추천 버튼 생성
        recommend_button = tk.Button(
            self.frame,
            text="요리 추천 받기",
            command=self.recommend_recipes,
            bg="#A5D6A7",
            fg="#1B5E20",
            font=("Aria", 14, "bold"),
            relief="raised",
            borderwidth=2
        )
        recommend_button.pack(pady=10)

        # 추천 결과를 표시할 레이블 생성
        self.recommendation_label = tk.Label(
            self.frame,
            text="",
            bg="#E3F2FD",
            fg="#0D47A1",
            font=("Aria", 14),
            anchor="w",
            justify="left",
            padx=10,
            pady=10,
            wraplength=400
        )
        self.recommendation_label.pack(fill="both", expand=True, pady=10)

    def get_user_ingredients(self):
        """냉장고, 냉동실, 실온 보관의 재료를 모두 가져옵니다."""
        ingredients = []
        # 냉장고 재료 가져오기
        if self.fridge:
            ingredients.extend(self.fridge.get_all_ingredients())
        # 냉동실 재료 가져오기
        if self.freezer:
            ingredients.extend(self.freezer.get_all_ingredients())
        # 실온 보관 재료 가져오기
        if self.room_temp:
            ingredients.extend(self.room_temp.get_all_ingredients())

        # 중복 재료 제거
        return list(set(ingredients))

    def translate_to_english(self, ingredients):
        """한국어 재료를 영어로 번역합니다."""
        # 자주 쓰이는 재료에 대한 수동 번역 사전
        manual_translation = {
            "감자": "potato",
            "양파": "onion",
            "당근": "carrot",
            "고추": "pepper",
            "마늘": "garlic",
            "토마토": "tomato",
            "치즈": "cheese",
            "시금치": "spinach",
            "닭고기": "chicken",
            "돼지고기": "pork",
            "소고기": "beef",
            "버섯": "mushroom",
            "생선": "fish",
            "밥": "rice",
            "계란": "egg",
            "우유": "milk",
            "소금": "salt",
            "설탕": "sugar",
            "간장": "soy sauce",
            "참기름": "sesame oil",
            "후추": "black pepper",
            "밀가루": "flour",
            "올리브유": "olive oil",
            "버터": "butter",
            "고춧가루": "red pepper powder",
            "간마늘": "minced garlic",
            "생강": "ginger",
            "대파": "green onion",
            "콩나물": "bean sprouts",
            "배추": "napa cabbage",
            "김치": "kimchi",
            "두부": "tofu",
            "된장": "soybean paste",
            "고추장": "red pepper paste",
            "참치": "tuna",
            "계란말이": "egg roll",
            "사과": "apple",
            "바나나": "banana",
            "딸기": "strawberry",
            "파프리카": "bell pepper",
            "양배추": "cabbage",
            "호박": "zucchini",
            "애호박": "korean zucchini",
            "오이": "cucumber",
            "가지": "eggplant",
            "옥수수": "corn",
            "연근": "lotus root",
            "미역": "seaweed",
            "떡": "rice cake",
            "쌀": "rice grain",
            "찹쌀": "glutinous rice",
            "라면": "ramen noodles",
            "당면": "glass noodles",
            "우동면": "udon noodles",
            "스파게티": "spaghetti",
            "소세지": "sausage",
            "베이컨": "bacon",
            "새우": "shrimp",
            "굴": "oyster",
            "멸치": "anchovy",
            "쌈장": "ssamjang",
            "레몬": "lemon",
            "라임": "lime",
            "오렌지": "orange",
            "포도": "grape",
            "키위": "kiwi",
            "배": "pear",
            "복숭아": "peach",
            "체리": "cherry",
            "고구마": "sweet potato",
            "밤": "chestnut",
            "무": "radish",
            "브로콜리": "broccoli",
            "양상추": "lettuce",
            "시리얼": "cereal",
            "연유": "condensed milk",
            "크림": "cream",
            "파슬리": "parsley",
            "로즈마리": "rosemary",
            "타임": "thyme",
            "바질": "basil",
            "오레가노": "oregano",
            "민트": "mint",
            "설탕시럽": "simple syrup",
            "식초": "vinegar",
            "흑설탕": "brown sugar",
            "꿀": "honey",
            "요거트": "yogurt",
            "베이킹파우더": "baking powder",
            "베이킹소다": "baking soda",
            "우스터소스": "worcestershire sauce",
            "토마토소스": "tomato sauce",
            "케첩": "ketchup",
            "마요네즈": "mayonnaise",
            "머스타드": "mustard",
            "칠리소스": "chili sauce",
            "두반장": "doubanjiang",
            "굴소스": "oyster sauce",
            "땅콩버터": "peanut butter",
            "아몬드": "almond",
            "호두": "walnut",
            "피스타치오": "pistachio",
            "캐슈넛": "cashew",
            "대추": "jujube",
            "건포도": "raisin",
            "잣": "pine nut",
            "들기름": "perilla oil",
            "참깨": "sesame seeds",
            "해바라기씨": "sunflower seeds",
            "아보카도": "avocado",
            "페퍼론치노": "pepperoncino",
            "코코넛밀크": "coconut milk",
            "코코넛오일": "coconut oil",
            "녹차가루": "matcha powder",
            "초콜릿": "chocolate",
            "화이트초콜릿": "white chocolate",
            "커피": "coffee",
            "카카오닙스": "cacao nibs",
            "버번": "bourbon",
            "와인": "wine",
            "맥주": "beer",
            "소주": "soju",
            "청주": "cheongju",
            "막걸리": "makgeolli",
            "고수": "coriander",
            "양고기": "lamb",
            "오리고기": "duck",
            "연어": "salmon",
            "명태": "pollock",
            "전복": "abalone",
            "바지락": "clams",
            "가리비": "scallops",
            "문어": "octopus",
            "쭈꾸미": "webfoot octopus",
            "홍합": "mussel",
            "오징어": "squid",
            "갈치": "hairtail",
            "삼치": "spanish mackerel",
            "고등어": "mackerel",
            "청양고추": "cheongyang chili pepper",
            "깻잎": "perilla leaf",
            "파": "leek",
            "쑥갓": "crown daisy",
            "매실청": "plum syrup",
            "황태": "dried pollack",
            "대추야자": "date palm",
            "퀴노아": "quinoa",
            "렌틸콩": "lentils",
            "병아리콩": "chickpeas",
            "검정콩": "black beans",
            "팥": "adzuki beans",
            "완두콩": "green peas",
            "아스파라거스": "asparagus",
            "리코타 치즈": "ricotta cheese",
            "모짜렐라 치즈": "mozzarella cheese",
            "파마산 치즈": "parmesan cheese",
            "크림치즈": "cream cheese",
            "치킨스톡": "chicken stock",
            "야채스톡": "vegetable stock",
            "다진 소고기": "ground beef",
            "새싹채소": "sprouts",
            "적양배추": "red cabbage",
            "수박": "watermelon",
            "아이스크림": "ice cream",
            "베이글": "bagel",
            "팬케이크": "pancake",
            "와플": "waffle",
            "허브": "herbs",
            "고구마 전분": "sweet potato starch",
            "콘시럽": "corn syrup",
            "스테이크 소스": "steak sauce",
            "디종 머스타드": "dijon mustard",
            "라즈베리": "raspberry",
            "블루베리": "blueberry",
            "크랜베리": "cranberry",
            "참깨소스": "sesame dressing",
            "탄산수": "sparkling water",
            "피망": "pimiento",
            "두리안": "durian",
            "오크라": "okra",
            "커리 가루": "curry powder",
            "인삼": "ginseng",
            "한라봉": "hallabong",
            "고추냉이": "wasabi",
            "레드와인 식초": "red wine vinegar",
            "흑미": "black rice",
            "푸실리": "fusilli",
            "펜네": "penne",
            "땅콩": "peanut",
            "메밀": "buckwheat",
            "수제비": "hand-pulled dough",
            "조미료": "seasoning",
            "타코야키 가루": "takoyaki flour",
            "크래커": "cracker",
            "플레인 요구르트": "plain yogurt",
            "타르타르소스": "tartar sauce",
            "붉은 강낭콩": "red kidney beans",
            "미소된장": "miso paste",
            "고추기름": "chili oil",
            "청양고추": "cheongyang chili",
            "조기": "yellow corvina",
            "대구": "codfish",
            "장어": "eel",
            "홍어": "fermented skate",
            "삼겹살": "pork belly",
            "대패삼겹살": "thinly sliced pork belly",
            "돼지갈비": "pork ribs",
            "소갈비": "beef ribs",
            "굴비": "dried yellow corvina",
            "차돌박이": "beef brisket",
            "칼국수 면": "knife-cut noodles",
            "도토리묵": "acorn jelly",
            "묵은지": "fermented kimchi",
            "장조림": "braised beef",
            "어묵": "fish cake",
            "곤약": "konjac",
            "열무": "young radish",
            "깍두기": "cubed radish kimchi",
            "수삼": "fresh ginseng",
            "겨자": "mustard paste",
            "부추": "chives",
            "전복죽": "abalone porridge",
            "꽁치": "pacific saury",
            "고등어조림": "braised mackerel",
            "쌀국수": "rice noodles",
            "매운탕": "spicy fish stew",
            "비지": "soy pulp",
            "팽이버섯": "enoki mushroom",
            "표고버섯": "shiitake mushroom",
            "송이버섯": "pine mushroom",
            "능이버섯": "neungi mushroom",
            "냉이": "shepherd's purse",
            "취나물": "aster scaber",
            "고사리": "bracken",
            "톳": "seaweed fusiforme",
            "감태": "laver",
            "우엉": "burdock root",
            "미나리": "water parsley",
            "대추": "jujube",
            "수삼": "fresh ginseng",
            "쑥": "mugwort",
            "다시마": "kelp",
            "명란젓": "salted pollock roe",
            "게장": "soy sauce marinated crab",
            "황석어젓": "yellow croaker sauce",
            "보리": "barley",
            "통밀": "whole wheat",
            "강낭콩": "kidney beans",
            "강황": "turmeric",
            "우거지": "outer cabbage leaves",
            "도라지": "balloon flower root",
            "멍게": "sea squirt",
            "미더덕": "sea squirt",
            "홍합탕": "mussel soup",
            "김밥용 김": "gimbap seaweed",
            "깻잎 장아찌": "pickled perilla leaves",
            "다대기": "spicy red pepper paste",
            "피클": "pickle",
            "아욱": "mallow",
            "방울토마토": "cherry tomato",
            "연두부": "silken tofu",
            "생크림": "heavy cream",
            "오징어젓갈": "salted squid",
            "복분자": "korean black raspberry",
            "홍시": "ripe persimmon",
            "황도": "yellow peach",
            "수수": "sorghum",
            "메밀묵": "buckwheat jelly",
            "막대과자": "pocky sticks",
            "도미": "sea bream",
            "돈까스소스": "tonkatsu sauce",
            "빼빼로": "pepero",
            "인절미": "injeolmi",
            "찰떡": "glutinous rice cake",
            "백김치": "white kimchi",
            "청국장": "fermented soybean paste",
            "굴림만두": "rolling dumplings",
            "비엔나소시지": "vienna sausage",
            "게맛살": "crab stick",
            "올리고당": "oligosaccharide syrup",
            "호떡믹스": "hotteok mix",
            "땅콩가루": "ground peanuts",
            "명란": "pollock roe",
            "복어": "pufferfish",
            "과메기": "dried half-dried fish",
            "사골": "beef bone",
            "쇠고기다시다": "beef bouillon",
            "누룽지": "scorched rice",
            "떡국떡": "rice cake for soup",
            "오징어채": "dried shredded squid",
            "닭발": "chicken feet",
            "닭가슴살": "chicken breast",
            "곱창": "intestines",
            "닭똥집": "chicken gizzard",
            "홍합살": "shelled mussel",
            "쥐포": "dried filefish",
            "생강청": "ginger syrup",
            "다시마물": "kelp broth",
            "애호박죽": "korean zucchini porridge",
            "백설기": "steamed rice cake",
            "곶감": "dried persimmon",
            "전병": "jeonbyeong",
            "모시조개": "clam",
            "꼬막": "cockle",
            "오리알": "duck egg",
            "부대찌개소스": "army stew sauce",
            "샤브샤브용 소고기": "beef for shabu-shabu",
            "떡볶이 떡": "tteokbokki rice cake",
            "호두파이": "walnut pie",
            "생크림 케이크": "whipped cream cake",
            "미숫가루": "misutgaru powder"
}


        translated_ingredients = []
        for ingredient in ingredients:
            if ingredient in manual_translation:
                translated_ingredients.append(manual_translation[ingredient])
            else:
                try:
                    translated = self.translator.translate(ingredient, src='ko', dest='en')
                    translated_ingredients.append(translated.text)
                except Exception as e:
                    print(f"재료 '{ingredient}'를 번역하는 중 오류가 발생했습니다: {e}")
                    continue  # 번역에 실패한 경우 다음 재료로 넘어감
        return translated_ingredients

    def recommend_recipes(self):
        """사용자가 가지고 있는 재료로 레시피를 추천합니다."""
        user_ingredients = self.get_user_ingredients()
        if not user_ingredients:
            messagebox.showwarning("재료 없음", "추천할 수 있는 재료가 없습니다. 냉장고, 냉동실, 실온에 재료를 추가하세요.")
            return

        # 재료를 영어로 번역
        translated_ingredients = self.translate_to_english(user_ingredients)
        if not translated_ingredients:
            messagebox.showwarning("번역 오류", "재료 번역에 실패했습니다. 다시 시도해 주세요.")
            return  # 번역에 실패한 경우 진행하지 않음

        # Spoonacular API URL 설정
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={','.join(translated_ingredients)}&apiKey={self.api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            recipes = response.json()

            if recipes:
                # 추천 요리 제목을 한국어로 번역
                translated_titles = []
                for recipe in recipes:
                    try:
                        translated = self.translator.translate(recipe['title'], src='en', dest='ko')
                        translated_titles.append(translated.text)
                    except Exception as e:
                        print(f"레시피 '{recipe['title']}'를 번역하는 중 오류가 발생했습니다: {e}")
                        translated_titles.append(recipe['title'])  # 번역 실패 시 원문 사용

                # 추천 결과를 화면에 표시
                message = "다음 요리를 추천합니다:\n" + "\n".join([f"- {title}" for title in translated_titles])
                self.recommendation_label.config(text=message)
            else:
                self.recommendation_label.config(text="보유한 재료로 만들 수 있는 요리가 없습니다.")

        except requests.RequestException as e:
            messagebox.showerror("오류", f"요리 추천 중 오류가 발생했습니다: {e}")

# 예시로 RecipeRecommendation 클래스 사용 (루트 윈도우 생성)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Recipe Recommendation Example")
    root.configure(bg="#E3F2FD")  # 루트 창 배경색 설정

    # 사용 예시 (테스트용 프레임 및 클래스들)
    class Fridge:
        def get_all_ingredients(self):
            return ["토마토", "양파", "치즈"]

    class Freezer:
        def get_all_ingredients(self):
            return ["닭고기", "시금치"]

    class RoomTemp:
        def get_all_ingredients(self):
            return ["감자", "마늘"]

    fridge = Fridge()
    freezer = Freezer()
    room_temp = RoomTemp()
    api_key = "40bc4817df984254aa6cc217d3ee6219"

    recipe_recommendation = RecipeRecommendation(root, fridge, freezer, room_temp, api_key)

    root.mainloop()
