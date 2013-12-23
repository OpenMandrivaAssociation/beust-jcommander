%_javapackages_macros
%global short_name   jcommander

Name:             beust-%{short_name}
Version:          1.30
Release:          4.0%{?dist}
Summary:          Java framework for parsing command line parameters
License:          ASL 2.0

URL:              http://jcommander.org/
Source0:          https://github.com/cbeust/%{short_name}/archive/%{short_name}-%{version}.tar.gz
BuildArch:        noarch
BuildRequires:    maven-local
BuildRequires:    beust-jcommander

%description
JCommander is a very small Java framework that makes it trivial to
parse command line parameters (with annotations).

%package javadoc
Summary:          API documentation for %{name}


%description javadoc
This package contains the %{summary}.

%prep
%setup -q -n %{short_name}-%{short_name}-%{version}
chmod -x license.txt

%build
%mvn_file : %{name}
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc license.txt notice.md README.markdown

%files javadoc -f .mfiles-javadoc
%doc license.txt notice.md

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.30-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Feb  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.30-2
- Replace BR: xmvn with maven-local

* Thu Jan 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.30-1
- Update to upstream version 1.30
- Build with xmvn

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.17-6
- Install NOTICE files

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.17-3
- Use the new maven macro.

* Mon May 16 2011 Jaromir Capik <jcapik@redhat.com> - 1.17-2
- Unwanted comment removal
- Target javadoc:jar replaced with javadoc:aggregate

* Fri May 13 2011 Jaromir Capik <jcapik@redhat.com> - 1.17-1
- Initial version of the package
