import re

def parse_dataset(filename):
    """Lê dataset e devolve dicionário estruturado."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    data = {'cc': {}, 'dsd': {}, 'tr': {}, 'rr': {}, 'oc': {}, 'olw': []}
    section = None

    for line in lines:
        line = line.replace('—', '-').strip()
        # identificar secções
        if line.lower().startswith('#cc'): section = 'cc'; continue
        elif line.lower().startswith('#dsd'): section = 'dsd'; continue
        elif line.lower().startswith('#tr'): section = 'tr'; continue
        elif line.lower().startswith('#rr'): section = 'rr'; continue
        elif line.lower().startswith('#oc'): section = 'oc'; continue
        elif line.lower().startswith('#olw'): section = 'olw'; continue
        elif line.lower().startswith('#head'): section = 'head'; continue
        if section == 'head': continue

        parts = re.split(r'\s+', line)
        if not parts: continue

        if section == 'cc':
            data['cc'][parts[0]] = parts[1:]
        elif section == 'dsd':
            for c in parts[1:]:
                data['dsd'][c] = parts[0]
        elif section == 'tr':
            data['tr'][parts[0]] = list(map(int, parts[1:]))
        elif section == 'rr':
            data['rr'][parts[0]] = parts[1]
        elif section == 'oc':
            data['oc'][parts[0]] = int(parts[1])

    return data

if __name__ == "__main__":
    from pprint import pprint
    dataset = parse_dataset("ClassTT_01_tiny.txt")
    pprint(dataset)
