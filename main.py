from datetime import datetime

from src.note_taker import NoteTaker
from src.terminal_utils import clear_screen


def note_cmd_check(notes: list[str], cmd: list[str]) -> bool:
    return len(notes) >= len(cmd) and notes[-1*len(cmd):] == cmd


def take_notes(app: NoteTaker) -> None:
    people: list[str] = app.randomize()
    i: int = 0

    while i < len(people):
        # Prevent bound issues
        i = min(max(0, i), len(people) - 1)

        person = people[i]

        print(f'Notes for {person}:')
        for note in app.get_notes_for_person(person):
            print(f'> {note}')
        while True:
            note = input('> ')
            app.add_note(person, note)

            notes = app.get_notes_for_person(person)
            if note_cmd_check(notes, ['', '']):
                i += 1
                break
            elif note_cmd_check(notes, ['g', 'b']):
                app.set_notes_for_person(person, notes[:-2])
                i -= 1
                break


def main() -> None:
    clear_screen()

    app = NoteTaker(__file__, empty_note='No notes or not present')
    app.log.toggle_print(False)

    take_notes(app)

    print()

    print(app.notes_as_md(True))
    date = datetime.now()

    file_name = f'notes{app.fs.separator}{date.date().isoformat()}' + \
        ("_t" if app.args.testing else "") + \
        (f'_{app.args.file}' if app.args.file != '' else "") + '.md'

    app.fs.write_file(file_name, app.notes_as_md(True), True)

    print(f'wrote to file: "{file_name}"')


def main2():
    app = NoteTaker(__file__, 'DEBUG')
    names = app.randomize()
    for name in names:
        app.add_note(name, 'note 1')
        app.add_note(name, 'note 2')
        app.add_note(name, 'note 3')
        app.add_note(name, 'note 4')
    app.add_note('JayBear 0', 'note 4 PR')

    print(app)
    print(app.notes_as_md(False))


if __name__ == '__main__':
    main()
