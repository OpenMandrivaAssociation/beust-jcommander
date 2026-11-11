Name:		beust-jcommander
Version:	2.0
Release:	2
Summary:	Command line parser driven by annotations
Group:		Development/Java
License:	Apache-2.0
URL:		https://jcommander.org/
Source0:	https://github.com/cbeust/jcommander/archive/refs/tags/%{version}.tar.gz#/jcommander-%{version}.tar.gz
# Gradle 9.9.1 strictly pins com.beust:jcommander 1.78. Wrapper jars
# are not in this archive. 2.0 stays the default jar.
Source1:	https://github.com/cbeust/jcommander/archive/refs/tags/1.78.tar.gz#/jcommander-1.78.tar.gz
BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	javapackages-filesystem
BuildRequires:	sysjar
Requires:	java-current

%description
JCommander turns annotated fields into command line options.
2.0 requires Java 11. The classes stay in com.beust.jcommander, and
the published Maven coordinate is org.jcommander:jcommander. The
previous com.beust:jcommander coordinate is installed as an alias of
2.0, and also as its own 1.78 jar. Gradle 9.9.1 strictly pins 1.78.

Since 1.48 the parser gained usage formatters, value validators,
and default providers. 2.0 also skips bridge and synthetic methods
when it looks for parameters, and a value may start with @.

%prep
%setup -q -n jcommander-%{version}
%setup -q -T -D -a 1 -n jcommander-%{version}
# Wrapper scripts ship prebuilt jars. The build does not use them.
find . -name '*.jar' -delete
find . -name '*.class' -delete
# Upstream marks the license executable. It is not a script.
chmod a-x license.txt
cp -p module-info.java src/main/java/module-info.java

%build
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
mkdir -p build/classes
find src/main/java -name '*.java' > build/sources.list
test -s build/sources.list
"$JAVA_HOME/bin/javac" --release 11 -proc:none -d build/classes @build/sources.list
cat > build/MANIFEST.MF << 'EOF'
Manifest-Version: 1.0
Implementation-Title: JCommander
Implementation-Version: %{version}
Implementation-Vendor: Cedric Beust
EOF
"$JAVA_HOME/bin/jar" cfm build/jcommander.jar build/MANIFEST.MF -C build/classes .
mkdir -p build/classes178
find jcommander-1.78/src/main/java -name '*.java' > build/sources178.list
test -s build/sources178.list
"$JAVA_HOME/bin/javac" --release 8 -proc:none -encoding UTF-8 -Xlint:-options \
	-d build/classes178 @build/sources178.list
"$JAVA_HOME/bin/jar" cf build/jcommander-1.78.jar -C build/classes178 .
cat > build/jcommander-1.78.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.beust</groupId>
  <artifactId>jcommander</artifactId>
  <version>1.78</version>
  <name>JCommander</name>
  <description>Command line parser driven by annotations.</description>
  <url>https://jcommander.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
</project>
EOF
test -s build/jcommander.jar
cat > build/jcommander.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.jcommander</groupId>
  <artifactId>jcommander</artifactId>
  <version>%{version}</version>
  <name>JCommander</name>
  <description>Command line parser driven by annotations.</description>
  <url>https://jcommander.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
      <distribution>repo</distribution>
    </license>
  </licenses>
</project>
EOF

%install
sysjar install --buildroot %{buildroot} \
	--artifact "build/jcommander.pom:build/jcommander.jar" \
	--file-name jcommander \
	--link %{name} \
	--alias com.beust:jcommander \
	--filelist .mfiles
sysjar install --buildroot %{buildroot} \
	--artifact "build/jcommander-1.78.pom:build/jcommander-1.78.jar" \
	--file-name jcommander-1.78 \
	--filelist .mfiles178
while IFS= read -r line; do
	grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
done < .mfiles178

%check
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
cat > JcSmoke.java << 'EOF'
import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
public class JcSmoke {
    @Parameter(names = "--name")
    String name = "unset";
    @Parameter(names = "--times")
    int times = 1;
    public static void main(String[] args) {
        JcSmoke smoke = new JcSmoke();
        JCommander.newBuilder().addObject(smoke).build().parse(args);
        if (!"ivy".equals(smoke.name) || smoke.times != 3) {
            throw new RuntimeException(smoke.name + " " + smoke.times);
        }
        System.out.println("jcommander ok");
    }
}
EOF
"$JAVA_HOME/bin/javac" --release 11 -proc:none -cp build/jcommander.jar JcSmoke.java
"$JAVA_HOME/bin/java" -cp "build/jcommander.jar:." JcSmoke --name ivy --times 3 > check.log
grep -F -q 'jcommander ok' check.log
"$JAVA_HOME/bin/jar" --describe-module --file build/jcommander.jar > check-module.log
grep -F -q 'com.beust.jcommander' check-module.log
cat > JcSmoke178.java << 'EOF'
import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
public class JcSmoke178 {
	@Parameter(names = "--n")
	int n;
	public static void main(String[] args) {
		JcSmoke178 smoke = new JcSmoke178();
		JCommander.newBuilder().addObject(smoke).build().parse("--n", "42");
		if (smoke.n != 42) {
			throw new AssertionError(smoke.n);
		}
		System.out.println("jcommander178_ok " + smoke.n);
	}
}
EOF
"$JAVA_HOME/bin/javac" --release 8 -proc:none -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/jcommander-1.78.jar JcSmoke178.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/jcommander-1.78.jar:." JcSmoke178 | tee check178.log
grep -F -q 'jcommander178_ok 42' check178.log

%files -f .mfiles
%license license.txt
%doc README.markdown CHANGELOG.md notice.md SECURITY.md
