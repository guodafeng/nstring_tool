import os
import re

class XliffEditor(object):
    def __init__(self, fname):
        self.fname = fname

    def clean_translation(self):
        '''
        clean the translation target element and save to fname trailed with
        'clean'
        '''
        out = []
        with open(self.fname, 'r', encoding='utf8') as f:
            for line in f.readlines():
                index = line.find('<target>')
                if index>0:
                    line = ' '*index + '<target/>\n'
                elif line.find('</target>') >=0:
                    line = '\n'
                    
                out.append(line)

        base_name, ext = os.path.splitext(self.fname)
        out_fname = base_name + '_clean' + ext
        with open(out_fname, 'w', encoding='utf8') as fw:
            fw.writelines(out)

    def better_clean(self):
        contents = ''
        with open(self.fname, 'r', encoding='utf8') as f:
            contents = f.read();
            pattern = re.compile('<target>.*?</target>', re.DOTALL)
            contents = re.sub(pattern, '<target/>', contents)

        base_name, ext = os.path.splitext(self.fname)
        out_fname = base_name + '_clean' + ext
        with open(out_fname, 'w', encoding='utf8') as fw:
            fw.write(contents)

def main():
    #test
    editor = XliffEditor('testfile/alb.xliff')
    editor.better_clean()

if __name__ == '__main__':
    main()
