import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import FileUpload from '../FileUpload';

// Mock the API
jest.mock('../../services/api', () => ({
  uploadVideo: jest.fn()
}));

import { uploadVideo } from '../../services/api';

describe('FileUpload Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders upload interface', () => {
    render(<FileUpload />);
    
    expect(screen.getByText('📹 Upload Videos')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /upload video/i })).toBeInTheDocument();
  });

  test('validates file type', () => {
    render(<FileUpload />);
    
    const fileInput = screen.getByLabelText(/choose file/i);
    const invalidFile = new File(['content'], 'test.txt', { type: 'text/plain' });
    
    fireEvent.change(fileInput, { target: { files: [invalidFile] } });
    
    expect(screen.getByText(/please select a video file/i)).toBeInTheDocument();
  });

  test('handles successful upload', async () => {
    uploadVideo.mockResolvedValue({
      success: true,
      video_no: 'test123',
      file_name: 'test.mp4',
      message: 'Upload successful'
    });

    render(<FileUpload />);
    
    const fileInput = screen.getByLabelText(/choose file/i);
    const validFile = new File(['content'], 'test.mp4', { type: 'video/mp4' });
    
    fireEvent.change(fileInput, { target: { files: [validFile] } });
    fireEvent.click(screen.getByRole('button', { name: /upload video/i }));

    await waitFor(() => {
      expect(screen.getByText(/upload successful/i)).toBeInTheDocument();
    });
  });
});
