from django.utils import timezone
from . import jalali
import os
from random import randint

def jalali_convertor(time):
    jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time = timezone.localtime(time)

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}, ساعت {time.hour}:{time.minute}'
    return persian_numbers(output)

def jalali_convertor_tokens(time):
    jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}'
    return persian_numbers(output)

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


# before function File storage
def get_filename_ext_rand(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random_1 = randint(1000, 9999)
    random_2 = randint(1000, 9999)
    return name, ext, f'{random_1}-{random_2}'

# ######### for doctors imgs ######### #
def doctor_image_path(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{instance.code}-{rand}{ext}"
    return f"doctors/{final_name}"

# ######### for patient imgs ######### #
def patient_image_path(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{instance.code}-{rand}{ext}"
    return f"patient/{final_name}"

# ######### for brands imgs ######### #
def brands_image_path(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{rand}{ext}"
    return f"brands/{final_name}"



# ######### for doctor codes ######### #
def get_doctor_code():
    random_1 = randint(1000, 9999)
    random_2 = randint(1000, 9999)
    return f'{random_1}{random_2}'

# ######### for patient codes ######### #
def get_patient_code():
    random_1 = randint(1000, 9999)
    random_2 = randint(1000, 9999)
    return f'{random_1}{random_2}'
