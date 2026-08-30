import json, os, subprocess

build_dir = '/home/ihriyasat/build_report'
tex_files = {
    'bibtex.bib': '6a79bc696508fd9ae098bd21',
    'main.tex': '6a79bc696508fd9ae098bd28',
    'entry_chapters/abstract.tex': '6a79bc696508fd9ae098bd22',
    'entry_chapters/acknowledgement.tex': '6a79bc696508fd9ae098bd23',
    'entry_chapters/attestation.tex': '6a79bc696508fd9ae098bd24',
    'entry_chapters/evaluation_committee.tex': '6a79bc696508fd9ae098bd25',
    'entry_chapters/letter_of_transmittal.tex': '6a79bc696508fd9ae098bd26',
    'entry_chapters/titlepage.tex': '6a79bc696508fd9ae098bd27',
    'primary_chapters/body_of_the_project.tex': '6a79bc696508fd9ae098bd29',
    'primary_chapters/consent_form.tex': '6a79bc696508fd9ae098bd2a',
    'primary_chapters/future_work_and_conclusion.tex': '6a79bc696508fd9ae098bd2b',
    'primary_chapters/introduction.tex': '6a79bc696508fd9ae098bd2c',
    'primary_chapters/lesson_learned.tex': '6a79bc696508fd9ae098bd2d',
    'primary_chapters/literature_review.tex': '6a79bc696508fd9ae098bd2e',
    'primary_chapters/methodology.tex': '6a79bc696508fd9ae098bd2f',
    'primary_chapters/project_as_engineering_problem_analysis.tex': '6a79bc696508fd9ae098bd31',
    'primary_chapters/project_management_and_financing.tex': '6a79bc696508fd9ae098bd33',
    'primary_chapters/results_and_analysis.tex': '6a79bc696508fd9ae098bd35'
}

js_lines = ["// Sync script"]
for rel_path, doc_id in tex_files.items():
    local_path = os.path.join(build_dir, rel_path)
    if os.path.exists(local_path):
        with open(local_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        
        escaped_lines = json.dumps(lines)
        stmt = (
            "var res = db.docs.updateOne("
            + "{_id: ObjectId('" + doc_id + "')}, "
            + "{$set: {lines: " + escaped_lines + "}, $inc: {version: 1}}"
            + ");\n"
            + "print('Synced " + rel_path + " -> matched: ' + res.matchedCount + ', modified: ' + res.modifiedCount);"
        )
        js_lines.append(stmt)

js_file = '/tmp/sync_all_clean.js'
with open(js_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_lines))

subprocess.run(['docker', 'cp', js_file, 'mongo:/tmp/sync_all_clean.js'], check=True)
res = subprocess.run(['docker', 'exec', '-i', 'mongo', 'mongosh', 'sharelatex', '--norc', '--quiet', '/tmp/sync_all_clean.js'], capture_output=True, text=True)
print(res.stdout)
