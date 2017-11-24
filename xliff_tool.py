import os

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



def main():
    #test
    editor = XliffEditor('testfile/alb.xliff')
    editor.clean_translation()

if __name__ == '__main__':
    main()
