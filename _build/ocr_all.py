import glob, os, subprocess, sys, tempfile
import pymupdf

ATT = "/home/user/.doubao/agent_mode/workspace/.sessions/38452402065600514/attachments"


def run(book_kw, outdir):
    f = [p for p in glob.glob(os.path.join(ATT, "*.pdf")) if book_kw in p][0]
    d = pymupdf.open(f)
    os.makedirs(outdir, exist_ok=True)
    for i in range(d.page_count):
        out = os.path.join(outdir, "p%03d.txt" % (i + 1))
        if os.path.exists(out) and os.path.getsize(out) > 0:
            continue
        png = os.path.join(tempfile.gettempdir(), "%s_%03d.png" % (book_kw, i + 1))
        d[i].get_pixmap(dpi=200).save(png)
        try:
            txt = subprocess.run(
                ["tesseract", png, "stdout", "-l", "chi_sim", "--psm", "6"],
                capture_output=True, text=True, timeout=120,
            ).stdout
        except subprocess.TimeoutExpired:
            txt = ""
        with open(out, "w") as fh:
            fh.write(txt)
        os.remove(png)
        print("%s p%d/%d len=%d" % (book_kw, i + 1, d.page_count, len(txt)), flush=True)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
