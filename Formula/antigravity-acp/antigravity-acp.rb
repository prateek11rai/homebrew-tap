class AntigravityAcp < Formula
  desc "Antigravity Agent Client Protocol (ACP) server"
  homepage "https://antigravity.google"
  version "1.4.1"

  on_macos do
    on_arm do
      url "https://dl.google.com/agy-extensions/releases/macos/agy-acp-server-1.4.1-darwin-arm64.zip"
      sha256 "f9bdd68291ae78c38d2141e63bc86b84e6cc7b9f60f71652c68435a7943deb17"
    end
    on_intel do
      url "https://dl.google.com/agy-extensions/releases/macos/agy-acp-server-1.4.1-darwin-x86_64.zip"
      sha256 "27e31f096874704f14167b07ef9e84cc77134615ee41d024f7b1c957add85307"
    end
  end

  on_linux do
    on_arm do
      url "https://dl.google.com/agy-extensions/releases/linux/agy-acp-server-1.4.1-linux-arm64.zip"
      sha256 "609336a1c97545487e3ddd55dbd153dc0f40f4e6534486cc1c5f4c0ebb85c2da"
    end
    on_intel do
      url "https://dl.google.com/agy-extensions/releases/linux/agy-acp-server-1.4.1-linux-x86_64.zip"
      sha256 "2e37012ceb2a5c7fc7309b6e6596234fb637ee3c62a5199f65d4cbe777871384"
    end
  end

  def install
    bin.install "agy_acp_server.par"
    bin.install "localharness_external"
  end

  test do
    assert_predicate bin/"agy_acp_server.par", :exist?
    assert_predicate bin/"localharness_external", :exist?
  end
end
