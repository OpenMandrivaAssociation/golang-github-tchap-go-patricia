%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 0
%global with_debug 0
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         tchap
%global repo            go-patricia
# https://github.com/tchap/go-patricia
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          f64d0a63cd3363481c898faa9339de04d12213f9
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-github-tchap-go-patricia
Version:        1.0.1
Release:        10%{?dist}
Summary:        A generic patricia trie implemented in Go
License:        MIT
URL:            https://%{import_path}
Source0:        https://%{import_path}/archive/v%{version}.tar.gz
BuildArch:      noarch

%description
A generic patricia trie (also called radix tree) implemented in Go (Golang).

The patricia trie as implemented in this library enables fast visiting of
items in some particular ways:

1. visit all items saved in the tree,
2. visit all items matching particular prefix (visit subtree), or
3. given a string, visit all items matching some prefix of that string.

%if 0%{?with_devel}
%package devel
Summary:        A golang registry for global request variables
BuildArch:     noarch

%if 0%{?with_check}
%endif

Provides:      golang(%{import_path}/patricia) = %{version}-%{release}

%description devel
A generic patricia trie (also called radix tree) implemented in Go (Golang).

The patricia trie as implemented in this library enables fast visiting of
items in some particular ways:

1. visit all items saved in the tree,
2. visit all items matching particular prefix (visit subtree), or
3. given a string, visit all items matching some prefix of that string.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test
Summary:         Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -n go-patricia-%{version}

%build

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/patricia
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test -f unit-test.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-9
- https://fedoraproject.org/wiki/Changes/golang1.7

* Wed Mar 16 2016 jchaloup <jchaloup@redhat.com> - 1.0.1-8
- Polish the spec file
  resolves: #1318341

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 30 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.1-4
- Resolves: rhbz#1117562 - package review request
- Remove conditional for fedora/rhel (separately deal with el6)

* Thu Jul 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.1-3
- disable debuginfo

* Wed Jul 16 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.1-2
- From: Vincent Batts <vbatts@fedoraproject.org>
- use macros from golang >= 1.2.1-3
- preserve timestamps of copied source
- do not own directories owned by golang

* Tue Jul 08 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.1-1
- Initial fedora package
