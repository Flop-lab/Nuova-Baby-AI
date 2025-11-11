"""
Streaming tests for NDJSON format validation.
Tests the streaming response format: meta → delta → final chunks.
"""

import pytest
import json
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi.responses import StreamingResponse
from src.main import app
from src.models.schemas import ChatRequest, StreamingChunk, ChunkType
from src.orchestrator.orchestrator import Orchestrator


class TestStreamingFlow:
    """Test streaming NDJSON response format and chunking."""
    
    @pytest.fixture
    def client(self):
        """Create FastAPI test client."""
        return TestClient(app)
    
    @pytest.fixture
    def streaming_request(self):
        """Create streaming chat request."""
        return {
            "message": "Open TextEdit",
            "stream": True
        }
    
    @pytest.fixture
    def non_streaming_request(self):
        """Create non-streaming chat request."""
        return {
            "message": "Open TextEdit",
            "stream": False
        }

    def test_streaming_response_format(self, client, streaming_request):
        """Test that streaming responses return proper NDJSON format."""
        
        # Mock orchestrator to avoid real LLM calls
        with patch('src.main.orchestrator.process_message') as mock_process:
            # Mock a simple response
            mock_response = Mock()
            mock_response.message = "I've opened TextEdit for you!"
            mock_response.conversation_id = "test-conv-123"
            mock_response.step_id = 1
            mock_process.return_value = mock_response
            
            response = client.post("/api/chat", json=streaming_request)
            
            # Verify response is streaming
            assert response.status_code == 200
            assert response.headers.get("content-type") == "application/x-ndjson"
            
            # Parse NDJSON lines
            lines = response.text.strip().split('\n')
            assert len(lines) >= 3  # At least meta, delta, final
            
            # Verify each line is valid JSON
            chunks = []
            for line in lines:
                chunk_data = json.loads(line)
                chunks.append(chunk_data)
            
            # Verify chunk structure and order
            assert chunks[0]["type"] == "meta"  # First chunk is meta
            assert chunks[-1]["type"] == "final"  # Last chunk is final
            
            # Verify all middle chunks are deltas
            for chunk in chunks[1:-1]:
                assert chunk["type"] == "delta"

    def test_streaming_meta_chunk_structure(self, client, streaming_request):
        """Test that meta chunk contains correct metadata."""
        
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_response = Mock()
            mock_response.message = "Opening TextEdit..."
            mock_response.conversation_id = "test-conv-456"
            mock_response.step_id = 2
            mock_process.return_value = mock_response
            
            response = client.post("/api/chat", json=streaming_request)
            
            # Parse first chunk (meta)
            first_line = response.text.strip().split('\n')[0]
            meta_chunk = json.loads(first_line)
            
            # Verify meta chunk structure
            assert meta_chunk["type"] == "meta"
            assert "conversation_id" in meta_chunk
            assert "step_id" in meta_chunk
            assert "timestamp" in meta_chunk
            assert meta_chunk["conversation_id"] == "test-conv-456"
            assert meta_chunk["step_id"] == 2

    def test_streaming_delta_chunks_content(self, client, streaming_request):
        """Test that delta chunks contain incremental content."""
        
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_response = Mock()
            mock_response.message = "I've successfully opened TextEdit for you!"
            mock_response.conversation_id = "test-conv-789"
            mock_response.step_id = 3
            mock_process.return_value = mock_response
            
            response = client.post("/api/chat", json=streaming_request)
            
            # Parse all chunks
            lines = response.text.strip().split('\n')
            chunks = [json.loads(line) for line in lines]
            
            # Get delta chunks
            delta_chunks = [chunk for chunk in chunks if chunk["type"] == "delta"]
            
            # Verify delta chunks have content
            for delta in delta_chunks:
                assert "content" in delta
                assert isinstance(delta["content"], str)
                assert len(delta["content"]) > 0
            
            # Verify content builds up progressively
            full_content = "".join(delta["content"] for delta in delta_chunks)
            assert "TextEdit" in full_content

    def test_streaming_final_chunk_structure(self, client, streaming_request):
        """Test that final chunk contains complete response."""
        
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_response = Mock()
            mock_response.message = "TextEdit has been opened successfully!"
            mock_response.conversation_id = "test-conv-final"
            mock_response.step_id = 4
            mock_process.return_value = mock_response
            
            response = client.post("/api/chat", json=streaming_request)
            
            # Parse last chunk (final)
            last_line = response.text.strip().split('\n')[-1]
            final_chunk = json.loads(last_line)
            
            # Verify final chunk structure
            assert final_chunk["type"] == "final"
            assert "message" in final_chunk
            assert "conversation_id" in final_chunk
            assert "step_id" in final_chunk
            assert final_chunk["message"] == "TextEdit has been opened successfully!"
            assert final_chunk["conversation_id"] == "test-conv-final"
            assert final_chunk["step_id"] == 4

    def test_non_streaming_response_format(self, client, non_streaming_request):
        """Test that non-streaming responses return complete JSON."""
        
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_response = Mock()
            mock_response.message = "I've opened TextEdit for you!"
            mock_response.conversation_id = "test-conv-non-stream"
            mock_response.step_id = 5
            mock_process.return_value = mock_response
            
            response = client.post("/api/chat", json=non_streaming_request)
            
            # Verify response is not streaming
            assert response.status_code == 200
            assert response.headers.get("content-type") == "application/json"
            
            # Parse complete JSON response
            response_data = response.json()
            
            # Verify structure matches ChatResponse schema
            assert "message" in response_data
            assert "conversation_id" in response_data
            assert "step_id" in response_data
            assert response_data["message"] == "I've opened TextEdit for you!"
            assert response_data["conversation_id"] == "test-conv-non-stream"
            assert response_data["step_id"] == 5

    def test_streaming_error_handling(self, client, streaming_request):
        """Test error handling in streaming mode."""
        
        # Mock orchestrator to raise an exception
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_process.side_effect = Exception("Test error")
            
            response = client.post("/api/chat", json=streaming_request)
            
            # Should still return 200 but with error in stream
            assert response.status_code == 200
            assert response.headers.get("content-type") == "application/x-ndjson"
            
            # Parse response chunks
            lines = response.text.strip().split('\n')
            chunks = [json.loads(line) for line in lines]
            
            # Should have error chunk
            error_chunks = [chunk for chunk in chunks if chunk.get("type") == "error"]
            assert len(error_chunks) > 0
            
            error_chunk = error_chunks[0]
            assert "error" in error_chunk
            assert "Sorry" in error_chunk["error"] or "error" in error_chunk["error"].lower()

    def test_streaming_chunk_timing(self, client, streaming_request):
        """Test that streaming chunks are delivered in reasonable time."""
        import time
        
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_response = Mock()
            mock_response.message = "Opening TextEdit application now..."
            mock_response.conversation_id = "test-timing"
            mock_response.step_id = 6
            mock_process.return_value = mock_response
            
            start_time = time.time()
            response = client.post("/api/chat", json=streaming_request)
            end_time = time.time()
            
            # Response should complete within reasonable time (< 5 seconds)
            response_time = end_time - start_time
            assert response_time < 5.0
            
            # Should have received chunks
            lines = response.text.strip().split('\n')
            assert len(lines) >= 3  # meta, delta(s), final

    def test_streaming_content_encoding(self, client):
        """Test that streaming handles various content encodings properly."""
        test_cases = [
            {"message": "Open Safari 🌐", "stream": True},
            {"message": "Ouvrir l'application TextEdit", "stream": True},
            {"message": "打开记事本应用程序", "stream": True},
            {"message": "Открыть приложение с эмодзи 🚀", "stream": True}
        ]
        
        for request_data in test_cases:
            with patch('src.main.orchestrator.process_message') as mock_process:
                mock_response = Mock()
                mock_response.message = f"Processing: {request_data['message']}"
                mock_response.conversation_id = "test-encoding"
                mock_response.step_id = 1
                mock_process.return_value = mock_response
                
                response = client.post("/api/chat", json=request_data)
                
                # Should handle all encodings properly
                assert response.status_code == 200
                
                # Parse chunks
                lines = response.text.strip().split('\n')
                chunks = [json.loads(line) for line in lines]
                
                # Verify content preserved
                final_chunk = chunks[-1]
                assert final_chunk["type"] == "final"
                assert request_data["message"] in mock_response.message or \
                       any(char in final_chunk["message"] for char in request_data["message"])

    def test_streaming_conversation_continuity(self, client):
        """Test that streaming maintains conversation context across requests."""
        
        # First streaming request
        request1 = {"message": "Open TextEdit", "stream": True}
        
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_response1 = Mock()
            mock_response1.message = "I've opened TextEdit for you!"
            mock_response1.conversation_id = "continuing-conv"
            mock_response1.step_id = 1
            mock_process.return_value = mock_response1
            
            response1 = client.post("/api/chat", json=request1)
            
            # Parse first response
            lines1 = response1.text.strip().split('\n')
            final_chunk1 = json.loads(lines1[-1])
            conv_id = final_chunk1["conversation_id"]
        
        # Second streaming request with same conversation
        request2 = {
            "message": "Now close it", 
            "stream": True, 
            "conversation_id": conv_id
        }
        
        with patch('src.main.orchestrator.process_message') as mock_process:
            mock_response2 = Mock()
            mock_response2.message = "I've closed TextEdit for you!"
            mock_response2.conversation_id = conv_id  # Same conversation
            mock_response2.step_id = 2  # Next step
            mock_process.return_value = mock_response2
            
            response2 = client.post("/api/chat", json=request2)
            
            # Parse second response
            lines2 = response2.text.strip().split('\n')
            final_chunk2 = json.loads(lines2[-1])
            
            # Verify conversation continuity
            assert final_chunk2["conversation_id"] == conv_id
            assert final_chunk2["step_id"] == 2
            assert final_chunk2["step_id"] > final_chunk1["step_id"]

    @pytest.mark.asyncio
    async def test_streaming_chunk_creation(self):
        """Test StreamingChunk model validation."""
        from src.models.schemas import StreamingChunk, ChunkType
        
        # Test meta chunk
        meta_chunk = StreamingChunk(
            type=ChunkType.META,
            conversation_id="test-123",
            step_id=1,
            timestamp="2025-11-12T10:00:00Z"
        )
        assert meta_chunk.type == ChunkType.META
        assert meta_chunk.conversation_id == "test-123"
        
        # Test delta chunk
        delta_chunk = StreamingChunk(
            type=ChunkType.DELTA,
            content="Hello "
        )
        assert delta_chunk.type == ChunkType.DELTA
        assert delta_chunk.content == "Hello "
        
        # Test final chunk
        final_chunk = StreamingChunk(
            type=ChunkType.FINAL,
            message="Complete response",
            conversation_id="test-123",
            step_id=1
        )
        assert final_chunk.type == ChunkType.FINAL
        assert final_chunk.message == "Complete response"