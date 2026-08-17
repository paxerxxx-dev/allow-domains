import os


if os.path.exists('changes/Russia/domains.lst'):
    with open('changes/Russia/domains.lst', 'r', encoding='utf-8') as f:
        domains = [line.strip() for line in f if line.strip()]
        with open ('changes/Russia/inside-dnsmasq-nfset.lst', 'w', encoding='utf-8') as f2:
            for domain in domains:
                if domain[0] != '#':
                    f2.write(f'nftset=/{domain.split("#")[0]}/4#inet#fw4#vpn_domains' + '\n')

# --- Создаем лист доменов ---
file = "changes/Russia/inside-dnsmasq-nfset.lst"
# Проверяем наличие вашего файла с личными доменами
if os.path.exists(file):
    target_file = 'Russia/inside-dnsmasq-nfset.lst'

    # Читаем домены из уже обновленного оригинального файла
    with open(target_file, 'r', encoding='utf-8') as f:
        existing_lines = set(line.strip() for line in f if line.strip())

    # Читаем ваши личные домены
    with open(file, 'r', encoding='utf-8') as f:
        custom_lines = [line.strip() for line in f if line.strip()]

    # Оставляем только те строки, которых нет в оригинале
    to_append = [line for line in custom_lines if line not in existing_lines]

    # Дописываем уникальные строки в конец
    if to_append:
        os.system('/bin/cp Russia/inside-dnsmasq-nfset.lst Openwrt/inside-dnsmasq-nfset.lst')
        with open('Openwrt/inside-dnsmasq-nfset.lst', 'a', encoding='utf-8') as f:
            for line in to_append:
                f.write(line + '\n')
        print(f'Файл inside-dnsmasq-nfset.lst обновлен')
        print(f"Успешно добавлено уникальных строк: {len(to_append)}")
    else:
        print("Все ваши домены уже есть в репозитории. Ничего не добавлено.")
else:
    print(f"Файл {file} не найден!")
    os.system('/bin/cp Russia/inside-dnsmasq-nfset.lst Openwrt/inside-dnsmasq-nfset.lst')


# --- Добавляем сети в nfset ---
subnets = ['discord.lst', 'telegram.lst', 'google_meet.lst']
with open('Openwrt/subnets.lst', 'w', encoding='utf-8') as f:
    for lst in subnets:
        if os.path.exists(f'Subnets/IPv4/{lst}'):
            with open(f'Subnets/IPv4/{lst}', 'r', encoding='utf-8') as l:
                lines = [line.strip() for line in l if line.strip()]
                for line in lines:
                    f.write(f'uci add_list firewall.@ipset[0].entry="{line}"' + '\n')
    if os.path.exists('changes/Russia/networks.lst'):
        with open('changes/Russia/networks.lst', 'r', encoding='utf-8') as l:
            lines = [line.strip() for line in l if line.strip()]
            for line in lines:
                if line[0] != "#":
                    f.write(f'uci add_list firewall.@ipset[0].entry="{line.split("#")[0]}"' + '\n')
    print(f'Файл Openwrt/subnets.lst обновлен')
