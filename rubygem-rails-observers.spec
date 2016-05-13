%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from rails-observers-0.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails-observers

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.1.2
Release: 8%{?dist}
Summary: Rails observer (removed from core in Rails 4.0)
Group: Development/Languages
License: MIT
URL: https://github.com/rails/rails-observers
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fixing tests for Rails 4.1+.
# https://github.com/rails/rails-observers/pull/26
Patch0: rubygem-rails-observers-0.1.2-substituting-ActiveRecord-TestCase-with-ActiveSupport-TestCase.patch

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix}rubygem(activemodel) => 4.0
Requires:      %{?scl_prefix}rubygem(activemodel) < 5
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
# Dependency is missing
#  - avoid unnecessary dependencies in SCL
#BuildRequires: %{?scl_prefix}rubygem(activerecord-deprecated_finders)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix}rubygem(rails) => 4.0
BuildRequires: %{?scl_prefix}rubygem(rails) < 5
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Rails observer (removed from core in Rails 4.0). ActiveModel::Observer,
ActiveRecord::Observer and ActionController::Caching::Sweeper extracted
from Rails.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

# Remove shebang from non-executable Rakefile
sed -i "/#\!\/usr\/bin\/env rake/d" Rakefile

%patch0 -p1

%build
%{?scl:scl enable %{scl} - << \EOF}
set -e
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Needs bundler
rm ./test/rake_test.rb

# Fix Mocha 1.x+ compatibility.
sed -i "/minitest/ a\require 'mocha/setup'" test/observing_test.rb

# Remove unavaliable depencency
sed -i '/activerecord-deprecated_finders/ s/^/#/' Gemfile

%{?scl:scl enable %{scl} - << \EOF}
set -e
ruby -Ilib:test -e "Dir.glob './test/*_test.rb', &method(:require)"
ruby -Ilib:test -e "Dir.glob './test/generators/*_test.rb', &method(:require)"
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%license %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/%{gem_name}.gemspec.erb
%{gem_instdir}/test

%changelog
* Thu Apr 07 2016 Pavel Valena <pvalena@redhat.com> - 0.1.2-8
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Josef Stribny <jstribny@redhat.com> - 0.1.2-5
- Fix tests

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 04 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-3
- Add mocha to build deps and enable test suite

* Thu Aug 01 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-2
- Improve the removal of the shebang
- fix the description and summary

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-1
- Initial package
