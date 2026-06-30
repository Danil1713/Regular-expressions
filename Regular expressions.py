
from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ
header = contacts_list[0]
phone_pattern = re.compile("(\+7|8)?\s*\(?(\d{3})\)?\s*(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})")
phone_replace = r"+7(\2)\3-\4-\5"
extra_pattern = re.compile(r"(доб\.?\s*(\d+))", re.IGNORECASE)
extra_replace = r"доб.\2"
for contact in contacts_list[1:]:
  fio = []
  for name in contact[:3]:
    if name.strip():
      parts = [p for p in name.split() if p.strip()]
      fio.extend(parts)
  contact[0] = fio[0] if len(fio) > 0 else ''
  contact[1] = fio[1] if len(fio) > 1 else ''
  contact[2] = fio[2] if len(fio) > 2 else ''

  if contact[5].strip():
    extra_match = extra_pattern.search(contact[5])
    extra = f" {extra_pattern.sub(extra_replace, extra_match.group(0))}" if extra_match else ''

    phone_match = phone_pattern.search(contact[5])
    if phone_match:
      formatted_phone = phone_pattern.sub(phone_replace, phone_match.group(0))
      contact[5] = formatted_phone + extra

contacts_dict = {}
for contact in contacts_list[1:]:
  key = (contact[0].lower(), contact[1].lower())
  if key not in contacts_dict:
    contacts_dict[key] = contact
  else:
    existing = contacts_dict[key]
    for i in range(len(contact)):
      if contact[i] and not existing[i]:
        existing[i] = contact[i]

contacts_list = [header] + list(contacts_dict.values())

pprint(contacts_list)
# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)