require 'net/http'
require 'json'

def generate_invite_code(size=7, chars=('a'..'z').to_a + ('A'..'Z').to_a + (0..9).to_a)
  size.times.map { chars.sample }.join
end

def check_invite(code)
  uri = URI("https://discordapp.com/api/v6/invites/#{code}")
  response = Net::HTTP.get_response(uri)
  if response.code == '200'
    JSON.parse(response.body)
  else
    nil
  end
end

def main
  while true
    codes = Array.new(4) { generate_invite_code }
    results = codes.map { |code| check_invite(code) }
    results.each_with_index do |server, index|
      if server
        puts "Found valid invite: #{codes[index]} for server '#{server['guild']['name']}'"
      end
    end
  end
end

main if __FILE__ == \$0
