%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from rails-observers-0.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails-observers

# ActiveModel 4.0
%global bootstrap 0

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.1.2
Release: 2%{?dist}
Summary: Rails observer (removed from core in Rails 4.0)
Group: Development/Languages
License: MIT
URL: https://github.com/rails/rails-observers
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(activemodel) => 4.0
Requires: %{?scl_prefix}rubygem(activemodel) < 5
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
%if 0%{bootstrap} < 1
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix}rubygem(activemodel) => 4.0
BuildRequires: %{?scl_prefix}rubygem(activemodel) < 5
%endif
BuildRequires: %{?scl_prefix_ruby}ruby
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

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
Documentation for %{pkg_name}

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

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if 0%{bootstrap} < 1
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
testrb -Ilib test/*_test.rb
%{?scl:EOF}
popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/%{gem_name}.gemspec.erb
%{gem_instdir}/test

%changelog
* Thu Aug 01 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-2
- Improve the removal of the shebang
- fix the description and summary

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-1
- Initial package
