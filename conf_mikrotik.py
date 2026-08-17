import os


# ---  Создаем конфиг листы из списка доменов ---
if os.path.exists('changes/Russia/domains.lst'):
    with open('changes/Russia/domains.lst', 'r', encoding='utf-8') as f:
        domains = [line.strip() for line in f if line.strip()]
        with open('changes/Russia/inside-mikrotik-fwd.lst', 'w', encoding='utf-8') as f2:
            for domain in domains:
                if domain[0] != '#':
                    if len(domain.split('#')) == 2:
                        comment = domain.split('#')[1]
                    else:
                        comment = ""
                    f2.write(f'/ip dns static add name={domain.split("#")[0]} type=FWD address-list=allow-domains match-subdomain=yes forward-to=localhost comment="{comment}"' + '\n')


# --- Создаем лист доменов ---
file = "changes/Russia/inside-mikrotik-fwd.lst"
# Проверяем наличие вашего файла с личными доменами
if os.path.exists(file):
    target_file = 'Russia/inside-mikrotik-fwd.lst'

    # Читаем домены из уже обновленного оригинального файла
    with open(target_file, 'r', encoding='utf-8') as f:
        existing_lines = set(line.strip() for line in f if line.strip())

    # Читаем ваши личные домены
    with open(file, 'r', encoding='utf-8') as f:
        custom_lines = [line.strip() for line in f if line.strip()]

    # Оставляем только те строки, которых нет в оригинале
    to_append = [line for line in custom_lines if " ".join(line.split()[0:-1]) not in existing_lines]

    # Дописываем уникальные строки в конец
    if to_append:
        os.system('/bin/cp Russia/inside-mikrotik-fwd.lst Mikrotik/inside-mikrotik-fwd.lst')
        with open('Mikrotik/inside-mikrotik-fwd.lst', 'a', encoding='utf-8') as f:
            f.write('# --- MY CUSTOM DOMAINS ---\n')
            for line in to_append:
                f.write(line + '\n')
        print(f'Файл Mikrotik/inside-mikrotik-fwd.lst обновлен')
        print(f"Успешно добавлено уникальных строк: {len(to_append)}")
    else:
        print("Все ваши домены уже есть в репозитории. Ничего не добавлено.")
else:
    print(f"Файл {file} не найден!")
    os.system('/bin/cp Russia/inside-mikrotik-fwd.lst Mikrotik/inside-mikrotik-fwd.lst')


# --- Создаем адрес лист ---
subnets = ['discord.lst', 'telegram.lst', 'google_meet.lst']
with open('Mikrotik/subnets.lst', 'w', encoding='utf-8') as f:
    for lst in subnets:
        if os.path.exists(f'Subnets/IPv4/{lst}'):
            with open(f'Subnets/IPv4/{lst}', 'r', encoding='utf-8') as l:
                lines = [line.strip() for line in l if line.strip()]
                for line in lines:
                    f.write(f'/ip/firewall/address-list/add address={line} comment="{lst}" list=allow-domains' + '\n')
    if os.path.exists('changes/Russia/networks.lst'):
        with open('changes/Russia/networks.lst', 'r', encoding='utf-8') as l:
            lines = [line.strip() for line in l if line.strip()]
            for line in lines:
                if line[0] != "#":
                    if len(line.split('#')) == 2:
                        comment = line.split('#')[1]
                    else:
                        comment = ""
                    f.write(f'/ip/firewall/address-list/add address={line.split("#")[0]} comment="{comment}" list=allow-domains' + '\n')
    print(f'Файл Mikrotik/subnets.lst обновлен')
