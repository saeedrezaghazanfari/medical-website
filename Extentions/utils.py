from django.utils import timezone
from . import jalali
import os
import datetime
from random import randint


def jalali_convertor(time, output='date_time', number=False):
    jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    time = timezone.localtime(time)

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    if number == True:
        time_to_list_num = list(time_to_tuple)
        for index, month in enumerate(intmonth):
            if time_to_list_num[1] == index + 1:
                time_to_list_num[1] = month
                break

    if output == 'date_time':        # ۲۱ دی ۱۴۰۰, ساعت ۲۱:۲۸
        output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}, ساعت {time.hour}:{time.minute}'
        return persian_numbers(output)
    elif output == 'j_date':         # ۲۱ دی ۱۴۰۰
        output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}'
        return persian_numbers(output)
    elif output == 'date' and number == True:           # ۲۱ - ۱۰ - ۱۴۰۰
        output = f'{time_to_list_num[2]} - {time_to_list_num[1]} - {time_to_list_num[0]}'
        return persian_numbers(output)
    elif output == 'j_month':        # دی 
        return persian_numbers(time_to_list[1])
    else:
        return 'No OutPut!'


def persian_numbers(myStr):
    numbers = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    for e, p in numbers.items():
        myStr = myStr.replace(e,p)
    return myStr

def get_ext_file(filename):
    extesion = os.path.splitext(str(filename))[1].lower()
    extesion_allowed = ['.png', '.jpg', 'jpeg']
    for i in extesion_allowed:
        if extesion == i:
            return 'yes'
    return 'no'


# =============== start static path

# before function File storage
def get_filename_ext_rand(filepath):
    time = datetime.datetime.now()
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(intmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random = randint(100, 999)
    output = f'{time_to_list[2]}{time_to_list[1]}{time_to_list[0]}{random}'
    return ext, output

# ######### for doctors imgs ######### #
def user_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"users/{final_name}"

# ######### for brands imgs ######### #
def brands_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"brands/{final_name}"

# ######### for blogs imgs ######### #
def blog_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"blogs/{final_name}"

# =============== end static path


# ######### get user code ######### #
def get_user_code():
    time = datetime.datetime.now()
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(intmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    random = randint(100, 999)
    output = f'{time_to_list[2]}{time_to_list[1]}{time_to_list[0]}{random}'
    return output
    # 21101400321 => 21 day, 10 month, 1400 age, 321 random
