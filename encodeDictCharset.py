#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
#################################################################
#
#  MeCab 用の辞書の文字コードを、任意の文字コードに変換する
#
#################################################################
 
import sys 
import shutil
import os
 
# http://docs.python.jp/2/library/argparse.html
import argparse
 
class MecabDictionaryEncoder:
    SUPPORTED_CHARSET = [
 'shift_jis', 'utf-8', 'euc_jp', 'cp932', 'euc_jis_2004','euc_jisx0213',
 'iso2022_jp','iso2022_jp_1', 'iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3',
 'iso2022_jp_ext', 'shift_jis_2004','shift_jisx0213','utf_16','utf_16_be',
 'utf_16_le','utf_7','utf_8_sig'
 ]   
    BACKUP_DIR = 'backup'
 
    def encodeDictFilesIn(self, dictDir, srcCharset, dstCharset):
        # オリジナルのファイルのバックアップ用ディレクトリを作る
        backupDir = os.path.join(dictDir, self.BACKUP_DIR)
        if not os.path.exists(backupDir):
            os.makedirs(backupDir)
        print 'backup original files to %s' % backupDir
 
        for file in os.listdir(dictDir):
            if file.endswith('.csv') or file.endswith('.def'):
                srcFile = os.path.join(dictDir, file)
                backupFile = os.path.join(backupDir, file)
 
                # 変換するファイルをバックアップする
                shutil.move(srcFile, backupFile)
 
                try:
                    # 指定の文字コードから変換する
                    self.encodeDictFile(backupFile, srcFile, srcCharset, dstCharset)
                except:
                    # 失敗した場合、文字コードを自動判定して変換する
                    for charset in self.SUPPORTED_CHARSET:
                        try:
                            self.encodeDictFile(backupFile, srcFile, charset, dstCharset)
                            break
                        except:
                            #raise
                            continue
                    else:
                        # 失敗したファイルは元にもどしておく
                        print 'failed to encode %s' % srcFile
                        shutil.move(backupFile, srcFile)
 
    def encodeDictFile(self, srcFile, dstFile, srcCharset, dstCharset):
        print 'encode %s from %s...' % (dstFile, srcCharset)
 
        try:
            src = open(srcFile, 'r')
            dst = open(dstFile, 'w')
 
            for line in src.readlines():
                line = line.decode(srcCharset)
                line = line.encode(dstCharset)
                dst.write(line)
        finally:
            if src:
                src.close()
            if dst:
                dst.close()
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MeCab の辞書の文字コードを任意の文字コードに変換する。変換対象のファイルは形態素を記載した .csv と、品詞の定義などを記載した .def になる。')
    parser.add_argument('-d', '--dictDir', metavar='dir', type=str, default='.', help='文字コードを変換する辞書が格納されているディレクトリ\nデフォルトではカレントディレクトリ')
    parser.add_argument('-s', '--srcCharset', metavar='charset', type=str, default='euc_jp', help='変換する辞書の現在の文字コード。この文字コードで辞書の読み取りに失敗した場合には自動検出が行われる。\nデフォルトでは EUC JP')
    parser.add_argument('-t', '--dstCharset', metavar='charset', type=str, default='utf-8', help='辞書の変換先文字コード\nデフォルトでは UTF8')
    args = parser.parse_args(sys.argv[1:])
 
    encoder = MecabDictionaryEncoder()
    encoder.encodeDictFilesIn(args.dictDir, args.srcCharset, args.dstCharset)