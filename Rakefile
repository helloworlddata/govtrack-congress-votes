require 'pathname'
DATA_DIR = Pathname 'catalog'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR.join('corral')
SCRIPTS = WRANGLE_DIR.join('scripts')
DIRS = {
    'fetched' => CORRAL_DIR / 'fetched',
    'compiled' => CORRAL_DIR / 'compiled',
    'published' => DATA_DIR,
}

MIN_CONGRESS = 98
MAX_CONGRESS = 114


F_FILES = {}
(MIN_CONGRESS..MAX_CONGRESS).each do |n|
  ['bills', 'votes'].each do |ctype|
      F_FILES["#{n}_#{ctype}"] = DIRS['fetched'].join('congress', n.to_s,  ctype)
   end
end


C_FILES = {}
(MIN_CONGRESS..MAX_CONGRESS).each do |n|
  ['bills', 'member_votes', 'votes'].each do |ctype|
      C_FILES["#{n}_#{ctype}"] = DIRS['compiled'].join('congress', n.to_s,  "#{ctype}.csv")
   end
end


desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        unless p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end

desc "Fetch everything"
task :fetch  => [:setup] do
  F_FILES.each_value{|fn| Rake::Task[fn].execute() }
end

desc "Compile everything"
task :compile  => [:setup] do
  C_FILES.each_value{|fn| Rake::Task[fn].execute() }
end

# desc "Publish everything"
# task :publish  => C_FILES.values() do
#   C_FILES.each_value do |fn|
#     sh %Q{
# cp #{fn} #{DIRS['published'] / fn.basename}
#     }
#   end
# end



namespace :files do


  namespace :compiled do
    C_FILES.each_value.select{|fn| fn.to_s =~ /votes\b/}.each do |fname|
      cgnum, ctype = fname.to_s.split('/').last(2).map{|p| p.to_s}
      desc "Compile #{ctype}.csv from Congress #{cgnum}"
      file fname => F_FILES["#{cgnum}_votes"] do
        puts fname
      end
    end
  end


  namespace :fetched do

    # e.g.
    # 'govtrack.us::govtrackdata/114/votes'
    SYNC_SRC = 'govtrack.us::govtrackdata/congress/%s/%s'

    F_FILES.each_value do |fname|
      cgnum, ctype = fname.to_s.split('/').last(2).map{|p| p.to_s}
      desc "rsync for #{ctype} from Congress #{cgnum}"
      file fname do
        fname.mkpath()
        syncsrc = SYNC_SRC % [cgnum, ctype]
        destpath = fname.parent
        cmd = %Q{
rsync -avz --delete --delete-excluded \
  --exclude **/text-versions/ \
  #{syncsrc} \
  #{destpath}
}
        sh cmd
      end
    end

  end
end
