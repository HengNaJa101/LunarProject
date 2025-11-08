#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Ecosystem Configuration Files
แก้ไข path ในไฟล์ ecosystem ทั้งหมดให้ใช้ C:\LunarProjectNew
"""

import os
import glob
import re

def update_ecosystem_files():
    """อัปเดต path ในไฟล์ ecosystem ทั้งหมด"""
    
    print("🔧 Update Ecosystem Configuration Files")
    print("=" * 50)
    
    # หาไฟล์ ecosystem ทั้งหมด
    ecosystem_files = glob.glob("ecosystem*.config.js")
    
    if not ecosystem_files:
        print("❌ ไม่พบไฟล์ ecosystem config")
        return False
    
    # Pattern สำหรับแทนที่
    old_patterns = [
        r"C:\\\\Users\\\\Administrator\\\\LunarProject",
        r"C:\\Users\\Administrator\\LunarProject",
    ]
    
    new_path = "C:\\\\LunarProjectNew"
    
    updated_files = []
    
    for file_path in ecosystem_files:
        try:
            print(f"📝 อัปเดตไฟล์: {file_path}")
            
            # อ่านไฟล์
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # แทนที่ path ทั้งหมด
            for pattern in old_patterns:
                content = re.sub(pattern, new_path, content)
            
            # ตรวจสอบว่ามีการเปลี่ยนแปลงหรือไม่
            if content != original_content:
                # เขียนไฟล์ใหม่
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ อัปเดต {file_path} สำเร็จ")
                updated_files.append(file_path)
            else:
                print(f"⚪ {file_path} ไม่ต้องอัปเดต")
                
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    if updated_files:
        print(f"\n🎯 อัปเดตสำเร็จ {len(updated_files)} ไฟล์:")
        for file_path in updated_files:
            print(f"   ✅ {file_path}")
        
        print(f"\n📁 Path ใหม่: C:\\LunarProjectNew")
        print("💡 ตอนนี้ PM2 จะใช้ path ที่ถูกต้องแล้ว")
        return True
    else:
        print("\n⚪ ไม่มีไฟล์ที่ต้องอัปเดต")
        return False

def show_current_config():
    """แสดงการตั้งค่าปัจจุบัน"""
    
    print("\n📋 ตรวจสอบการตั้งค่าปัจจุบัน:")
    print("-" * 30)
    
    ecosystem_files = glob.glob("ecosystem*.config.js")
    
    for file_path in ecosystem_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n📄 {file_path}:")
            
            # หา cwd และ interpreter
            cwd_matches = re.findall(r"cwd:\s*['\"]([^'\"]+)['\"]", content)
            interpreter_matches = re.findall(r"interpreter:\s*['\"]([^'\"]+)['\"]", content)
            
            for cwd in set(cwd_matches):
                print(f"   📁 cwd: {cwd}")
            
            for interpreter in set(interpreter_matches):
                print(f"   🐍 interpreter: {interpreter}")
                
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")

if __name__ == "__main__":
    print("🚀 Ecosystem Configuration Updater")
    print("=" * 60)
    
    # แสดงการตั้งค่าปัจจุบัน
    show_current_config()
    
    # อัปเดตไฟล์
    success = update_ecosystem_files()
    
    if success:
        # แสดงการตั้งค่าหลังอัปเดต
        print("\n" + "=" * 60)
        show_current_config()
        
        print("\n🎯 เสร็จสิ้น! PM2 พร้อมใช้งานบน C:\\LunarProjectNew")
    else:
        print("\n❌ การอัปเดตล้มเหลว")