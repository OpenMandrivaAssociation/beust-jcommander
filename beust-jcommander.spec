Name:		beust-jcommander
Version:	1.48
Release:	1
Summary:	Command line parser driven by annotations
Group:		Development/Java
License:	ASL 2.0
URL:		https://jcommander.org/
Source0:	https://github.com/cbeust/jcommander/archive/refs/tags/jcommander-%{version}.tar.gz#/jcommander-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	mvn(org.sonatype.oss:oss-parent:pom::)
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name jcommander --link %{name}

%description
JCommander turns annotated fields into command line options.
1.48 keeps enum values in their declared case, lets a main parameter
override its default, and no longer closes System.in from the
default console.

%prep
%autosetup -n jcommander-jcommander-%{version}

%files -f .mfiles
%doc CHANGELOG license.txt notice.md README.markdown
