import re

video_id_prog = re.compile(r'v=([^&]+)')
youtube_prog = re.compile(r'youtube\.com')
be_prog = re.compile(r'youtu.be/(\S+)$')


def get_ids_from_hvids_filename(filename):
    ids = []
    lines = [line.rstrip('\n') for line in open(filename, 'r')]
    for line in lines:
        if youtube_prog.search(line):
            if video_id_prog.search(line):
                search_id = video_id_prog.search(line).group(1)
                assert len(search_id) == 11
                ids.append(search_id)
        elif be_prog.search(line):
            search_id = be_prog.search(line).group(1)
            assert len(search_id) == 11
            ids.append(search_id)
    ids = list(set(ids))
    print(len(ids))
    return ids


if __name__ == '__main__':
    get_ids_from_hvids_filename('dHvidsLinks.txt')
