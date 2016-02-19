require 'formula'

class LINKS < Formula
  homepage 'https://github.com/dvirdi/links/'

  def install
    setup_args = ['setup.py', 'install']
    system "python", *setup_args
  end

  def scripts_folder
    HOMEBREW_PREFIX/"share/python"
  end

  def caveats
    <<-EOS.undent
      To run the `links` command, you'll need to add Python's script directory to your PATH:
        #{scripts_folder}
    EOS
  end
end