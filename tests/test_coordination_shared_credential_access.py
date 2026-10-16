from pathlib import Path


AGENTS = Path("AGENTS.md")
README = Path("README.md")
START_HERE = Path("coordination/START_HERE.md")
DIRECTIVE = Path("coordination/directives/GITHUB_NATIVE_DATA_ACCESS.md")


def test_root_agent_entrypoint_routes_to_shared_access_directive():
    text = AGENTS.read_text(encoding="utf-8").lower()
    assert "coordination/start_here.md" in text
    assert "github_native_data_access.md" in text
    assert "do not search" in text and ".env" in text
    assert "github actions" in text
    assert "plaintext" in text


def test_root_readme_no_longer_routes_provider_api_keys_to_local_env():
    text = README.read_text(encoding="utf-8").lower()
    assert "coordination/start_here.md" in text
    assert "github_native_data_access.md" in text
    assert "provider api credentials" in text and "github actions secrets" in text
    assert "plant admin" in text and "local" in text
    assert "api keys, passwords, webhook tokens, broker credentials | local secret manager or local `.env`" not in text


def test_start_here_routes_every_chat_to_github_native_data_plane():
    text = START_HERE.read_text(encoding="utf-8").lower()
    assert "github-native credential" in text
    assert "do not search" in text and ".env" in text
    assert "agent_credentials.md" in text
    assert "github_native_credentials.md" in text
    assert "config/data_ingestion_manifest.json" in text
    assert "github actions" in text
    assert "plaintext" in text and "not" in text


def test_shared_access_directive_explains_use_without_secret_possession():
    text = DIRECTIVE.read_text(encoding="utf-8").lower()
    assert "secret possession" in text
    assert "data access" in text
    assert "agents are not expected to read" in text
    assert "automation_intelligence/provider_collection_v1/latest" in text
    assert "automation_intelligence/provider_collection_v1/research_context.json" in text
    assert "config/data_ingestion_manifest.json" in text
    assert "github-native-credential-health" in text
    assert "provider-exhaustive-collection" in text
    assert "provider-supplemental-collection" in text
    assert "unusual whales" in text
    assert "finnhub" in text
    assert "401" in text
    assert "do not ask another ai" in text
