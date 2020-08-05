from scrapy.utils.log import logger
import psycopg2 as psycopg2

from cansoCrawler.utilities.Normalize import remove_extra_character_and_normalize
from cansoCrawler.utilities.Normalize import normalize_text
from cansoCrawler.utilities.configs import server_db, local_db

# db_config = local_db
db_config = server_db
conn = psycopg2.connect(
    database=db_config["database"],
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    port=db_config["port"])
cursor = conn.cursor()


def get_province(city: str):
    city = normalize_text(city)
    condition = create_city_condition(city)
    try:
        cursor.execute(
            f"select name from api_province where id=(select province_id from api_city where {condition} limit 1) limit 1"
        )
        data = cursor.fetchall()
        return data[0][0]
    except Exception as e:
        conn.rollback()
        logger.critical(f"get_province for {condition}: {e}")
        return 'not_defined'


def create_city_condition(city):
    condition = ""
    city = remove_extra_character_and_normalize(city)

    if city.find('ا') == 0 or city.find('آ') == 0:
        condition += f"( name = 'آ{city[1:]}' or name = 'ا{city[1:]}' )"
    else:
        condition += f"( name = '{city}' )"

    return condition


def get_last_url(table, source_id):
    try:
        cursor.execute(f"select url from {table} where source_id = {source_id} order by time desc limit 1")
        data = cursor.fetchall()
        logger.info(f"last url:{data[0][0]} for table:{table} and source:{source_id}")
        return data[0][0]
    except:
        conn.rollback()
        logger.critical(f"not find item for table:{table} and source:{source_id}")
        return None


PROVINCE_DATA = {
    "آذربایجان شرقی": [
        "تبریز",
        "اسکو",
        "اهر",
        "ایلخچی",
        "آبش احمد",
        "آذرشهر",
        "آقکند",
        "باسمنج",
        "بخشایش",
        "بستان آباد",
        "بناب",
        "بناب جدید",
        "ترک",
        "ترکمانچای",
        "تسوج",
        "تیکمه داش",
        "جلفا",
        "خاروانا",
        "خامنه",
        "خراجو",
        "خسروشهر",
        "خمارلو",
        "خواجه",
        "دوزدوزان",
        "زرنق",
        "زنوز",
        "سراب",
        "سردرود",
        "سیس",
        "سیه رود",
        "شبستر",
        "شربیان",
        "شرفخانه",
        "شندآباد",
        "شهرجدیدسهند",
        "صوفیان",
        "عجب شیر",
        "قره آغاج",
        "کشکسرای",
        "کلوانق",
        "کلیبر",
        "کوزه کنان",
        "گوگان",
        "لیلان",
        "مراغه",
        "مرند",
        "ملکان",
        "ممقان",
        "مهربان",
        "میانه",
        "نظرکهریزی",
        "وایقان",
        "ورزقان",
        "هادیشهر",
        "هریس",
        "هشترود",
        "هوراند",
        "یامچی"
    ],
    "آذربایجان غربی": [
        "ارومیه",
        "اشنویه",
        "ایواوغلی",
        "آواجیق",
        "باروق",
        "بازرگان",
        "بوکان",
        "پلدشت",
        "پیرانشهر",
        "تازه شهر",
        "تکاب",
        "چهاربرج",
        "خلیفان",
        "خوی",
        "دیزج دیز",
        "ربط",
        "سردشت",
        "سرو",
        "سلماس",
        "سیلوانه",
        "سیمینه",
        "سیه چشمه",
        "شاهین دژ",
        "شوط",
        "فیرورق",
        "قره ضیاءالدین",
        "قطور",
        "قوشچی",
        "کشاورز",
        "گردکشانه",
        "ماکو",
        "محمدیار",
        "محمودآباد",
        "مهاباد",
        "میاندوآب",
        "میرآباد",
        "نالوس",
        "نقده",
        "نوشین"
    ],
    "اردبیل": [
        "اردبیل",
        "اصلاندوز",
        "آبی بیگلو",
        "بیله سوار",
        "پارس آباد",
        "تازه کند",
        "تازه کندانگوت",
        "جعفرآباد",
        "خلخال",
        "رضی",
        "سرعین",
        "عنبران",
        "فخرآباد",
        "کلور",
        "کوراییم",
        "گرمی",
        "گیوی",
        "لاهرود",
        "مرادلو",
        "مشگین شهر",
        "نمین",
        "نیر",
        "هشتجین",
        "هیر"
    ],
    "اصفهان": [
        "اصفهان",
        "ابریشم",
        "ابوزیدآباد",
        "اردستان",
        "اژیه",
        "افوس",
        "انارک",
        "ایمانشهر",
        "آران وبیدگل",
        "بادرود",
        "باغ بهادران",
        "بافران",
        "برزک",
        "برف انبار",
        "بوئین ومیاندشت",
        "بهاران شهر",
        "بهارستان",
        "پیربکران",
        "تودشک",
        "تیران",
        "جندق",
        "جوزدان",
        "جوشقان وکامو",
        "چادگان",
        "چرمهین",
        "چمگردان",
        "حبیب آباد",
        "حسن آباد",
        "حنا",
        "خالدآباد",
        "خمینی شهر",
        "خوانسار",
        "خور",
        "خوراسگان",
        "خورزوق",
        "داران",
        "دامنه",
        "درچه پیاز",
        "دستگرد",
        "دولت آباد",
        "دهاقان",
        "دهق",
        "دیزیچه",
        "رزوه",
        "رضوانشهر",
        "زاینده رود",
        "زرین شهر",
        "زواره",
        "زیباشهر",
        "سده لنجان",
        "سفیدشهر",
        "سگزی",
        "سمیرم",
        "شاپورآباد",
        "شاهین شهر",
        "شهرضا",
        "طالخونچه",
        "عسگران",
        "علویچه",
        "فرخی",
        "فریدونشهر",
        "فلاورجان",
        "فولادشهر",
        "قمصر",
        "قهجاورستان",
        "قهدریجان",
        "کاشان",
        "کرکوند",
        "کلیشادوسودرجان",
        "کمشچه",
        "کمه",
        "کوشک",
        "کوهپایه",
        "کهریزسنگ",
        "گرگاب",
        "گزبرخوار",
        "گلپایگان",
        "گلدشت",
        "گلشن",
        "گلشهر",
        "گوگد",
        "لای بید",
        "مبارکه",
        "محمدآباد",
        "مشکات",
        "منظریه",
        "مهاباد",
        "میمه",
        "نائین",
        "نجف آباد",
        "نصرآباد",
        "نطنز",
        "نوش آباد",
        "نیاسر",
        "نیک آباد",
        "ورزنه",
        "ورنامخواست",
        "وزوان",
        "ونک",
        "هرند"
    ],
    "البرز": [
        "کرج",
        "اشتهارد",
        "آسارا",
        "تنکمان",
        "چهارباغ",
        "سیف آباد",
        "شهرجدیدهشتگرد",
        "طالقان",
        "کمال شهر",
        "کوهسار",
        "گرمدره",
        "ماهدشت",
        "محمدشهر",
        "مشکین دشت",
        "نظرآباد",
        "هشتگرد"
    ],
    "ایلام": [
        "ایلام",
        "ارکواز",
        "ایوان",
        "آبدانان",
        "آسمان آباد",
        "بدره",
        "پهله",
        "توحید",
        "چوار",
        "دره شهر",
        "دلگشا",
        "دهلران",
        "زرنه",
        "سراب باغ",
        "سرابله",
        "صالح آباد",
        "لومار",
        "مورموری",
        "موسیان",
        "مهران",
        "میمه"
    ],
    "بوشهر": [
        "بوشهر",
        "امام حسن",
        "انارستان",
        "اهرم",
        "آبپخش",
        "آبدان",
        "برازجان",
        "بردخون",
        "بردستان",
        "بندر دیر",
        "بندر دیلم",
        "بندر ریگ",
        "بندر کنگان",
        "بندر گناوه",
        "بنک",
        "تنگ ارم",
        "جم",
        "چغادک",
        "خارک",
        "خورموج",
        "دالکی",
        "دلوار",
        "ریز",
        "سعدآباد",
        "سیراف",
        "شبانکاره",
        "شنبه",
        "عسلویه",
        "کاکی",
        "کلمه",
        "نخل تقی",
        "وحدتیه"
    ],
    "تهران": [
        "تهران",
        "ارجمند",
        "اسلامشهر",
        "اندیشه",
        "آبسرد",
        "آبعلی",
        "باغستان",
        "باقرشهر",
        "بومهن",
        "پاکدشت",
        "پردیس",
        "پیشوا",
        "تجریش",
        "جوادآباد",
        "چهاردانگه",
        "حسن آباد",
        "دماوند",
        "رباط کریم",
        "رودهن",
        "ری",
        "شاهدشهر",
        "شریف آباد",
        "شهریار",
        "صالح آباد",
        "صباشهر",
        "صفادشت",
        "فردوسیه",
        "فرون آباد",
        "فشم",
        "فیروزکوه",
        "قدس",
        "قرچک",
        "کهریزک",
        "کیلان",
        "گلستان",
        "لواسان",
        "ملارد",
        "نسیم شهر",
        "نصیرآباد",
        "وحیدیه",
        "ورامین"
    ],
    "چهارمحال بختیاری": [
        "شهرکرد",
        "اردل",
        "آلونی",
        "باباحیدر",
        "بروجن",
        "بلداجی",
        "بن",
        "جونقان",
        "چلگرد",
        "سامان",
        "سفیددشت",
        "سودجان",
        "سورشجان",
        "شلمزار",
        "طاقانک",
        "فارسان",
        "فرادنبه",
        "فرخ شهر",
        "کیان",
        "گندمان",
        "گهرو",
        "لردگان",
        "مال خلیفه",
        "ناغان",
        "نافچ",
        "نقنه",
        "هفشجان"
    ],
    "خراسان جنوبی": [
        "بیرجند",
        "ارسک",
        "اسدیه",
        "اسفدن",
        "اسلامیه",
        "آرین شهر",
        "آیسک",
        "بشرویه",
        "حاجی آباد",
        "خضری دشت بیاض",
        "خوسف",
        "زهان",
        "سرایان",
        "سربیشه",
        "سه قلعه",
        "شوسف",
        "طبس مسینا",
        "فردوس",
        "قائن",
        "قهستان",
        "گزیک",
        "محمدشهر",
        "مود",
        "نهبندان",
        "نیمبلوک"
    ],
    "خراسان رضوی": [
        "مشهد",
        "احمدآبادصولت",
        "انابد",
        "باجگیران",
        "باخرز",
        "بار",
        "بایگ",
        "بجستان",
        "بردسکن",
        "بیدخت",
        "تایباد",
        "تربت جام",
        "تربت حیدریه",
        "جغتای",
        "جنگل",
        "چاپشلو",
        "چکنه",
        "چناران",
        "خرو",
        "خلیل آباد",
        "خواف",
        "داورزن",
        "درگز",
        "درود",
        "دولت آباد",
        "رباط سنگ",
        "رشتخوار",
        "رضویه",
        "روداب",
        "ریوش",
        "سبزوار",
        "سرخس",
        "سفیدسنگ",
        "سلامی",
        "سلطان آباد",
        "سنگان",
        "شادمهر",
        "شاندیز",
        "ششتمد",
        "شهرآباد",
        "شهرزو",
        "صالح آباد",
        "طرقبه",
        "عشق آباد",
        "فرهادگرد",
        "فریمان",
        "فیروزه",
        "فیض آباد",
        "قاسم آباد",
        "قدمگاه",
        "قلندرآباد",
        "قوچان",
        "کاخک",
        "کاریز",
        "کاشمر",
        "کدکن",
        "کلات",
        "کندر",
        "گلمکان",
        "گناباد",
        "لطف آباد",
        "مزدآوند",
        "مشهدریزه",
        "ملک آباد",
        "نشتیفان",
        "نصرآباد",
        "نقاب",
        "نوخندان",
        "نیشابور",
        "نیل شهر",
        "همت آباد",
        "یونسی"
    ],
    "خراسان شمالی": [
        "بجنورد",
        "اسفراین",
        "ایور",
        "آشخانه",
        "پیش قلعه",
        "تیتکانلو",
        "جاجرم",
        "حصارگرمخان",
        "درق",
        "راز",
        "سنخواست",
        "شوقان",
        "شیروان",
        "صفی آباد",
        "فاروج",
        "قاضی",
        "گرمه",
        "لوجلی"
    ],
    "خوزستان": [
        "اهواز",
        "اروندکنار",
        "الوان",
        "امیدیه",
        "اندیمشک",
        "ایذه",
        "آبادان",
        "آغاجاری",
        "باغ ملک",
        "بستان",
        "بندر امام خمینی",
        "بندر ماهشهر",
        "بهبهان",
        "ترکالکی",
        "جایزان",
        "جنت مکان",
        "چغامیش",
        "چمران",
        "چوئبده",
        "حر",
        "حسینیه",
        "حمزه",
        "حمیدیه",
        "خرمشهر",
        "دارخوین",
        "دزآب",
        "دزفول",
        "دهدز",
        "رامشیر",
        "رامهرمز",
        "رفیع",
        "زهره",
        "سالند",
        "سردشت",
        "سماله",
        "سوسنگرد",
        "شادگان",
        "شاوور",
        "شرافت",
        "شوش",
        "شوشتر",
        "شیبان",
        "صالح شهر",
        "صالح مشطط",
        "صفی آباد",
        "صیدون",
        "قلعه تل",
        "قلعه خواجه",
        "گتوند",
        "گوریه",
        "لالی",
        "مسجدسلیمان",
        "مشراگه",
        "مقاومت",
        "ملاثانی",
        "میانرود",
        "میداود",
        "مینوشهر",
        "ویس",
        "هفتگل",
        "هندیجان",
        "هویزه"
    ],
    "زنجان": [
        "زنجان",
        "ابهر",
        "ارمغانخانه",
        "آب بر",
        "چورزق",
        "حلب",
        "خرمدره",
        "دندی",
        "زرین آباد",
        "زرین رود",
        "سجاس",
        "سلطانیه",
        "سهرورد",
        "صائین قلعه",
        "قیدار",
        "گرماب",
        "ماه نشان",
        "هیدج"
    ],
    "سمنان": [
        "سمنان",
        "امیریه",
        "ایوانکی",
        "آرادان",
        "بسطام",
        "بیارجمند",
        "دامغان",
        "درجزین",
        "دیباج",
        "سرخه",
        "شاهرود",
        "شهمیرزاد",
        "کلاته خیج",
        "گرمسار",
        "مجن",
        "مهدی شهر",
        "میامی"
    ],
    "سیستان و بلوچستان": [
        "زاهدان",
        "ادیمی",
        "اسپکه",
        "ایرانشهر",
        "بزمان",
        "بمپور",
        "بنت",
        "بنجار",
        "پیشین",
        "جالق",
        "چاه بهار",
        "خاش",
        "دوست محمد",
        "راسک",
        "زابل",
        "زابلی",
        "زرآباد",
        "زهک",
        "سراوان",
        "سرباز",
        "سوران",
        "سیرکان",
        "علی اکبر",
        "فنوج",
        "قصرقند",
        "کنارک",
        "گشت",
        "گلمورتی",
        "محمدان",
        "محمدآباد",
        "محمدی",
        "میرجاوه",
        "نصرت آباد",
        "نگور",
        "نوک آباد",
        "نیک شهر",
        "هیدوج"
    ],
    "فارس": [
        "شیراز",
        "اردکان",
        "ارسنجان",
        "استهبان",
        "اسیر",
        "اشکنان",
        "افزر",
        "اقلید",
        "امام شهر",
        "اوز",
        "اهل",
        "ایج",
        "ایزدخواست",
        "آباده",
        "آباده طشک",
        "باب انار",
        "بالاده",
        "بنارویه",
        "بوانات",
        "بهمن",
        "بیرم",
        "بیضا",
        "جنت شهر",
        "جویم",
        "جهرم",
        "حاجی آباد",
        "حسامی",
        "حسن آباد",
        "خانه زنیان",
        "خاوران",
        "خرامه",
        "خشت",
        "خنج",
        "خور",
        "خومه زار",
        "داراب",
        "داریان",
        "دبیران",
        "دژکرد",
        "دوبرجی",
        "دوزه",
        "دهرم",
        "رامجرد",
        "رونیز",
        "زاهدشهر",
        "زرقان",
        "سده",
        "سروستان",
        "سعادت شهر",
        "سورمق",
        "سیدان",
        "ششده",
        "شهر جدید صدرا",
        "شهرپیر",
        "صغاد",
        "صفاشهر",
        "علامرودشت",
        "عمادده",
        "فدامی",
        "فراشبند",
        "فسا",
        "فیروزآباد",
        "قادرآباد",
        "قائمیه",
        "قطب آباد",
        "قطرویه",
        "قیر",
        "کارزین",
        "کازرون",
        "کامفیروز",
        "کره ای",
        "کنارتخته",
        "کوار",
        "کوهنجان",
        "گراش",
        "گله دار",
        "لار",
        "لامرد",
        "لپوئی",
        "لطیفی",
        "مبارک آباد",
        "مرودشت",
        "مشکان",
        "مصیری",
        "مهر",
        "میمند",
        "نوبندگان",
        "نوجین",
        "نودان",
        "نورآباد",
        "نی ریز",
        "وراوی",
        "هماشهر"
    ],
    "قزوین": [
        "قزوین",
        "ارداق",
        "اسفرورین",
        "اقبالیه",
        "الوند",
        "آبگرم",
        "آبیک",
        "آوج",
        "بوئین زهرا",
        "بیدستان",
        "تاکستان",
        "خاکعلی",
        "خرمدشت",
        "دانسفهان",
        "رازمیان",
        "سگزآباد",
        "سیردان",
        "شال",
        "شریفیه",
        "ضیاءآباد",
        "کوهین",
        "محمدیه",
        "محمودآبادنمونه",
        "معلم کلایه",
        "نرجه"
    ],
    "قم": [
        "قم",
        "جعفریه",
        "دستجرد",
        "سلفچگان",
        "قنوات",
        "کهک"
    ],
    "کردستان": [
        "سنندج",
        "آرمرده",
        "بابارشانی",
        "بانه",
        "بلبان آباد",
        "بوئین سفلی",
        "بیجار",
        "چناره",
        "دزج",
        "دلبران",
        "دهگلان",
        "دیواندره",
        "زرینه",
        "سروآباد",
        "سریش آباد",
        "سقز",
        "شویشه",
        "صاحب",
        "قروه",
        "کامیاران",
        "کانی دینار",
        "کانی سور",
        "مریوان",
        "موچش",
        "یاسوکند"
    ],
    "کرمان": [
        "کرمان",
        "اختیارآباد",
        "ارزوئیه",
        "امین شهر",
        "انار",
        "اندوهجرد",
        "باغین",
        "بافت",
        "بردسیر",
        "بروات",
        "بزنجان",
        "بم",
        "بهرمان",
        "پاریز",
        "جبالبارز",
        "جوپار",
        "جوزم",
        "جیرفت",
        "چترود",
        "خاتون آباد",
        "خانوک",
        "خورسند",
        "درب بهشت",
        "دوساری",
        "دهج",
        "رابر",
        "راور",
        "راین",
        "رفسنجان",
        "رودبار",
        "ریحان شهر",
        "زرند",
        "زنگی آباد",
        "زیدآباد",
        "سرچشمه",
        "سیرجان",
        "شهداد",
        "شهربابک",
        "صفائیه",
        "عنبرآباد",
        "فاریاب",
        "فهرج",
        "قلعه گنج",
        "کاظم آباد",
        "کشکوئیه",
        "کوهبنان",
        "کهنوج",
        "کیانشهر",
        "گلباف",
        "گلزار",
        "لاله زار",
        "ماهان",
        "محمدآباد",
        "محی آباد",
        "مردهک",
        "منوجان",
        "نجف شهر",
        "نرماشیر",
        "نظام شهر",
        "نگار",
        "نودژ",
        "هجدک",
        "هماشهر",
        "یزدان شهر"
    ],
    "کرمانشاه": [
        "کرمانشاه",
        "ازگله",
        "اسلام آبادغرب",
        "باینگان",
        "بیستون",
        "پاوه",
        "تازه آباد",
        "جوانرود",
        "حمیل",
        "رباط",
        "روانسر",
        "سرپل ذهاب",
        "سرمست",
        "سطر",
        "سنقر",
        "سومار",
        "شاهو",
        "صحنه",
        "قصرشیرین",
        "کرندغرب",
        "کنگاور",
        "کوزران",
        "گهواره",
        "گیلانغرب",
        "میان راهان",
        "نودشه",
        "نوسود",
        "هرسین",
        "هلشی"
    ],
    "کهکیلویه و بویراحمد": [
        "یاسوج",
        "باشت",
        "پاتاوه",
        "چرام",
        "چیتاب",
        "دوگنبدان",
        "دهدشت",
        "دیشموک",
        "سوق",
        "سی سخت",
        "قلعه رئیسی",
        "گراب سفلی",
        "لنده",
        "لیکک",
        "مادوان",
        "مارگون"
    ],
    "گلستان": [
        "گرگان",
        "انبارآلوم",
        "اینچه برون",
        "آزادشهر",
        "آق قلا",
        "بندر گز",
        "ترکمن",
        "جلین",
        "خان ببین",
        "دلند",
        "رامیان",
        "سرخنکلاته",
        "سیمین شهر",
        "علی آباد",
        "فاضل آباد",
        "کردکوی",
        "کلاله",
        "گالیکش",
        "گمیش تپه",
        "گنبد کاووس",
        "مراوه تپه",
        "مینودشت",
        "نگین شهر",
        "نوده خاندوز",
        "نوکنده"
    ],
    "گیلان": [
        "رشت",
        "احمدسرگوراب",
        "اسالم",
        "اطاقور",
        "املش",
        "آستارا",
        "آستانه اشرفیه",
        "بازارجمعه",
        "بره سر",
        "بندر انزلی",
        "پره سر",
        "تونکابن",
        "جیرنده",
        "چابکسر",
        "چاف وچمخاله",
        "چوبر",
        "حویق",
        "خشکبیجار",
        "خمام",
        "دیلمان",
        "رانکوه",
        "رحیم آباد",
        "رستم آباد",
        "رضوانشهر",
        "رودبار",
        "رودبنه",
        "رودسر",
        "سنگر",
        "سیاهکل",
        "شفت",
        "شلمان",
        "صومعه سرا",
        "فومن",
        "کلاچای",
        "کوچصفهان",
        "کومله",
        "کیاشهر",
        "گوراب زرمیخ",
        "لاهیجان",
        "لشت نشاء",
        "لنگرود",
        "لوشان",
        "لولمان",
        "لوندویل",
        "لیسار",
        "ماسال",
        "ماسوله",
        "مرجقل",
        "منجیل",
        "واجارگاه",
        "هشتپر"
    ],
    "لرستان": [
        "خرم آباد",
        "ازنا",
        "اشترینان",
        "الشتر",
        "الیگودرز",
        "بروجرد",
        "پلدختر",
        "چالانچولان",
        "چغلوندی",
        "چقابل",
        "درب گنبد",
        "دورود",
        "زاغه",
        "سپیددشت",
        "سراب دوره",
        "شول آباد",
        "فیروزآباد",
        "کونانی",
        "کوهدشت",
        "گراب",
        "معمولان",
        "مؤمن آباد",
        "نورآباد",
        "ویسیان",
        "هفت چشمه"
    ],
    "مازندران": [
        "ساری",
        "امیرکلا",
        "ایزدشهر",
        "آلاشت",
        "آمل",
        "بابل",
        "بابلسر",
        "بلده",
        "بهشهر",
        "بهنمیر",
        "پل سفید",
        "پول",
        "تنکابن",
        "جویبار",
        "چالوس",
        "چمستان",
        "خرم آباد",
        "خلیل شهر",
        "خوش رودپی",
        "دابودشت",
        "رامسر",
        "رستمکلا",
        "رویان",
        "رینه",
        "زرگر محله",
        "زیرآب",
        "سرخرود",
        "سلمان شهر",
        "سورک",
        "شیرگاه",
        "شیرود",
        "عباس آباد",
        "فریدونکنار",
        "فریم",
        "قائم شهر",
        "کتالم وسادات شهر",
        "کلارآباد",
        "کلاردشت",
        "کله بست",
        "کوهی خیل",
        "کیاسر",
        "کیاکلا",
        "گتاب",
        "گزنک",
        "گلوگاه",
        "محمودآباد",
        "مرزن آباد",
        "مرزیکلا",
        "نشتارود",
        "نکا",
        "نور",
        "نوشهر"
    ],
    "مرکزی": [
        "اراک",
        "آستانه",
        "آشتیان",
        "پرندک",
        "تفرش",
        "توره",
        "جاورسیان",
        "خشکرود",
        "خمین",
        "خنداب",
        "داودآباد",
        "دلیجان",
        "رازقان",
        "زاویه",
        "ساروق",
        "ساوه",
        "سنجان",
        "شازند",
        "شهرجدیدمهاجران",
        "غرق آباد",
        "فرمهین",
        "قورچی باشی",
        "کرهرود",
        "کمیجان",
        "مأمونیه",
        "محلات",
        "میلاجرد",
        "نراق",
        "نوبران",
        "نیمور",
        "هندودر"
    ],
    "هرمزگان": [
        "بندر عباس",
        "ابوموسی",
        "بستک",
        "بندر جاسک",
        "بندر چارک",
        "بندر لنگه",
        "بیکاه",
        "پارسیان",
        "تخت",
        "جناح",
        "حاجی آباد",
        "خمیر",
        "درگهان",
        "دهبارز",
        "رویدر",
        "زیارتعلی",
        "سردشت بشاگرد",
        "سرگز",
        "سندرک",
        "سوزا",
        "سیریک",
        "فارغان",
        "فین",
        "قشم",
        "قلعه قاضی",
        "کنگ",
        "کوشکنار",
        "کیش",
        "گوهران",
        "میناب",
        "هرمز",
        "هشتبندی"
    ],
    "همدان": [
        "همدان",
        "ازندریان",
        "اسدآباد",
        "برزول",
        "بهار",
        "تویسرکان",
        "جورقان",
        "جوکار",
        "دمق",
        "رزن",
        "زنگنه",
        "سامن",
        "سرکان",
        "شیرین سو",
        "صالح آباد",
        "فامنین",
        "فرسفج",
        "فیروزان",
        "قروه در جزین",
        "قهاوند",
        "کبودرآهنگ",
        "گل تپه",
        "گیان",
        "لالجین",
        "مریانج",
        "ملایر",
        "نهاوند"
    ],
    "یزد": [
        "یزد",
        "ابرکوه",
        "احمدآباد",
        "اردکان",
        "اشکذر",
        "بافق",
        "بفروئیه",
        "بهاباد",
        "تفت",
        "حمیدیا",
        "خضرآباد",
        "دیهوک",
        "زارچ",
        "شاهدیه",
        "طبس",
        "عشق آباد",
        "عقدا",
        "مروست",
        "مهردشت",
        "مهریز",
        "میبد",
        "ندوشن",
        "نیر",
        "هرات"
    ]
}
