# ☕ Java Runtime Upgrade Complete! 

## ✅ Current Status
- **Java 21.0.8 LTS** is now active in this terminal session
- **Java 8** and **Java 21** are both installed on your system
- Location: `C:\Program Files\Eclipse Adoptium\jdk-21.0.8.9-hotspot\`

## 🔧 Make Java 21 Permanent Default

### Option 1: Using Windows Settings (GUI)
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click **"Advanced"** tab → **"Environment Variables"**
3. In **"System Variables"** section:
   - **Add/Edit JAVA_HOME**:
     - Variable: `JAVA_HOME`
     - Value: `C:\Program Files\Eclipse Adoptium\jdk-21.0.8.9-hotspot`
   - **Edit PATH**:
     - Find: `C:\Program Files\Eclipse Foundation\jdk-8.0.302.8-hotspot\bin`
     - Remove it or move `%JAVA_HOME%\bin` to the top
4. Click **"OK"** to save
5. Restart Command Prompt/PowerShell

### Option 2: Using PowerShell (Admin Required)
```powershell
# Set JAVA_HOME permanently
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Eclipse Adoptium\jdk-21.0.8.9-hotspot", "Machine")

# Update PATH to prioritize Java 21
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
$newPath = $currentPath -replace "C:\\Program Files\\Eclipse Foundation\\jdk-8\.0\.302\.8-hotspot\\bin;", ""
$newPath = "%JAVA_HOME%\bin;" + $newPath
[Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
```

## 📊 Verification Commands
```bash
# Check Java version
java -version

# Check JAVA_HOME
echo %JAVA_HOME%

# Check javac compiler
javac -version

# Check installed JRE/JDK
where java
```

## 🚀 Java 21 LTS Features You Can Now Use
- **Pattern Matching for switch** (Preview → Standard)
- **Records** (Java 14+ feature now stable)
- **Text Blocks** (Java 15+ feature)
- **Virtual Threads** (Java 21 LTS headline feature)
- **Sequenced Collections** (Java 21)
- **String Templates** (Preview in Java 21)
- **Vector API** (Incubator)
- **Foreign Function & Memory API** (Preview)

## 🎯 Next Steps
1. ✅ Java 21 LTS successfully activated
2. 🔄 Make permanent using Option 1 or 2 above
3. ✅ Ready for modern Java development!

---
**Note**: Keep Java 8 installed if you have legacy applications that require it. You can always switch between versions by changing JAVA_HOME.