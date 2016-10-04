#!/usr/bin/env python3

import os
import tempfile
import re
import git


# Look for "include" sections in RST file and inline the referenced file(s)
def parse_rst_includes(rst_dir, rst_file):
  ii = 0
  with tempfile.NamedTemporaryFile(mode='w', dir=rst_dir, delete=False) as tmp, open(rst_dir + '/' + rst_file, 'r') as rst:
    for line in rst:
      if ii == 0:
        m = start_re.match(line)
        if m:
          ii = 1 - ii
          tmp.write(line)
          tmp.write('\n')
          with open(m.group(1), 'r') as inc:
            tmp.write('.. ' + m.group(2) + '\n\n')
            for line in inc:
              tmp.write('  ' + line)
            tmp.write('\n')
        else:
          tmp.write(line)
      else:
        m = end_re.match(line)
        if m:
          ii = 1 - ii
          tmp.write(line)
        else:
          pass

  os.replace(tmp.name, rst.name)

# Stage the RST file in git
  index.add([rst.name])


env = os.environ
#repo_root = env['PWD'][:(len(env['PWD'])-len(env['GIT_PREFIX']))]
#repo = git.Repo(repo_root)
repo = git.Repo(search_parent_directories=True)
repo_root = repo.working_dir
index = repo.index
start_re = re.compile(r'^\.\. include\s+([\w\.]+)\s+(\w+::.*)\s*$')
end_re = re.compile(r'^\.\. /include\s+([\w\.]+)$')


for root, dirs, files in os.walk(repo_root):
  if '.git' in dirs:
    dirs.remove('.git')
  for f in files:
    if f.endswith('.rst'):
      parse_rst_includes(root, f)

# Commit the git changes
index.commit("Updated RST includes")

