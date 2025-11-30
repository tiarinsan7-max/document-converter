import React, { useState } from 'react';
import {
  ChakraProvider,
  Box,
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  Button,
  Select,
  Progress,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Badge,
  Divider,
  useToast,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Card,
  CardHeader,
  CardBody,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
} from '@chakra-ui/react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { FiUpload, FiDownload, FiFile, FiCheckCircle } from 'react-icons/fi';

function App() {
  const [files, setFiles] = useState([]);
  const [outputFormat, setOutputFormat] = useState('pdf');
  const [quality, setQuality] = useState('high');
  const [converting, setConverting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState([]);
  const [formats, setFormats] = useState([]);
  const toast = useToast();

  // Fetch supported formats on mount
  React.useEffect(() => {
    fetchFormats();
  }, []);

  const fetchFormats = async () => {
    try {
      const response = await axios.get('/api/v1/formats');
      setFormats(response.data.formats);
    } catch (error) {
      console.error('Failed to fetch formats:', error);
    }
  };

  const onDrop = (acceptedFiles) => {
    setFiles(acceptedFiles);
    setResults([]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'application/json': ['.json'],
      'text/plain': ['.txt'],
    },
  });

  const handleConvert = async () => {
    if (files.length === 0) {
      toast({
        title: 'No files selected',
        description: 'Please upload files to convert',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setConverting(true);
    setProgress(0);
    setResults([]);

    try {
      if (files.length === 1) {
        // Single file conversion
        const formData = new FormData();
        formData.append('file', files[0]);
        formData.append('output_format', outputFormat);
        formData.append('quality', quality);

        const response = await axios.post('/api/v1/convert', formData, {
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(percentCompleted);
          },
        });

        setResults([response.data]);
        
        toast({
          title: 'Conversion successful!',
          description: `File converted to ${outputFormat.toUpperCase()}`,
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
      } else {
        // Batch conversion
        const formData = new FormData();
        files.forEach((file) => {
          formData.append('files', file);
        });
        formData.append('output_format', outputFormat);
        formData.append('quality', quality);

        const response = await axios.post('/api/v1/batch-convert', formData, {
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(percentCompleted);
          },
        });

        setResults(response.data.results);
        
        toast({
          title: 'Batch conversion complete!',
          description: `${response.data.successful} of ${response.data.total_files} files converted`,
          status: response.data.failed > 0 ? 'warning' : 'success',
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      toast({
        title: 'Conversion failed',
        description: error.response?.data?.message || error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setConverting(false);
      setProgress(100);
    }
  };

  const handleDownload = async (filename) => {
    try {
      const response = await axios.get(`/api/v1/download/${filename}`, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();

      toast({
        title: 'Download started',
        status: 'info',
        duration: 2000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Download failed',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <ChakraProvider>
      <Box bg="gray.50" minH="100vh" py={8}>
        <Container maxW="container.xl">
          {/* Header */}
          <VStack spacing={4} mb={8}>
            <Heading size="2xl" color="blue.600">
              📄 Universal Document Converter
            </Heading>
            <Text fontSize="lg" color="gray.600">
              Convert between PDF, DOCX, XLSX, CSV, JSON, and TXT
            </Text>
          </VStack>

          <Tabs colorScheme="blue" variant="enclosed">
            <TabList>
              <Tab>🔄 Convert</Tab>
              <Tab>📊 Formats</Tab>
              <Tab>ℹ️ About</Tab>
            </TabList>

            <TabPanels>
              {/* Convert Tab */}
              <TabPanel>
                <VStack spacing={6} align="stretch">
                  {/* Upload Area */}
                  <Card>
                    <CardHeader>
                      <Heading size="md">Upload Files</Heading>
                    </CardHeader>
                    <CardBody>
                      <Box
                        {...getRootProps()}
                        p={10}
                        border="2px dashed"
                        borderColor={isDragActive ? 'blue.400' : 'gray.300'}
                        borderRadius="lg"
                        bg={isDragActive ? 'blue.50' : 'white'}
                        cursor="pointer"
                        transition="all 0.2s"
                        _hover={{ borderColor: 'blue.400', bg: 'blue.50' }}
                      >
                        <input {...getInputProps()} />
                        <VStack spacing={3}>
                          <FiUpload size={48} color="#3182CE" />
                          <Text fontSize="lg" fontWeight="medium">
                            {isDragActive
                              ? 'Drop files here...'
                              : 'Drag & drop files here, or click to select'}
                          </Text>
                          <Text fontSize="sm" color="gray.500">
                            Supports: PDF, DOCX, XLSX, CSV, JSON, TXT
                          </Text>
                        </VStack>
                      </Box>

                      {files.length > 0 && (
                        <Box mt={4}>
                          <Text fontWeight="medium" mb={2}>
                            Selected Files ({files.length}):
                          </Text>
                          <VStack align="stretch" spacing={2}>
                            {files.map((file, index) => (
                              <HStack
                                key={index}
                                p={3}
                                bg="gray.50"
                                borderRadius="md"
                                justify="space-between"
                              >
                                <HStack>
                                  <FiFile />
                                  <Text>{file.name}</Text>
                                </HStack>
                                <Badge colorScheme="blue">
                                  {(file.size / 1024).toFixed(2)} KB
                                </Badge>
                              </HStack>
                            ))}
                          </VStack>
                        </Box>
                      )}
                    </CardBody>
                  </Card>

                  {/* Settings */}
                  <Card>
                    <CardHeader>
                      <Heading size="md">Conversion Settings</Heading>
                    </CardHeader>
                    <CardBody>
                      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                        <Box>
                          <Text mb={2} fontWeight="medium">
                            Output Format
                          </Text>
                          <Select
                            value={outputFormat}
                            onChange={(e) => setOutputFormat(e.target.value)}
                            size="lg"
                          >
                            {formats.map((format) => (
                              <option key={format} value={format}>
                                {format.toUpperCase()}
                              </option>
                            ))}
                          </Select>
                        </Box>

                        <Box>
                          <Text mb={2} fontWeight="medium">
                            Quality
                          </Text>
                          <Select
                            value={quality}
                            onChange={(e) => setQuality(e.target.value)}
                            size="lg"
                          >
                            <option value="low">Low (Fast)</option>
                            <option value="medium">Medium</option>
                            <option value="high">High (Best Quality)</option>
                          </Select>
                        </Box>
                      </SimpleGrid>
                    </CardBody>
                  </Card>

                  {/* Convert Button */}
                  <Button
                    colorScheme="blue"
                    size="lg"
                    onClick={handleConvert}
                    isLoading={converting}
                    loadingText="Converting..."
                    isDisabled={files.length === 0}
                  >
                    🚀 Convert Files
                  </Button>

                  {/* Progress */}
                  {converting && (
                    <Box>
                      <Text mb={2}>Converting files...</Text>
                      <Progress value={progress} colorScheme="blue" hasStripe isAnimated />
                    </Box>
                  )}

                  {/* Results */}
                  {results.length > 0 && (
                    <Card>
                      <CardHeader>
                        <Heading size="md">Conversion Results</Heading>
                      </CardHeader>
                      <CardBody>
                        <VStack align="stretch" spacing={3}>
                          {results.map((result, index) => (
                            <Box
                              key={index}
                              p={4}
                              bg={result.status === 'success' ? 'green.50' : 'red.50'}
                              borderRadius="md"
                              border="1px solid"
                              borderColor={result.status === 'success' ? 'green.200' : 'red.200'}
                            >
                              <HStack justify="space-between">
                                <HStack>
                                  {result.status === 'success' ? (
                                    <FiCheckCircle color="green" />
                                  ) : (
                                    <FiFile color="red" />
                                  )}
                                  <Text fontWeight="medium">
                                    {result.filename || result.output_file}
                                  </Text>
                                </HStack>
                                {result.status === 'success' && result.download_url && (
                                  <Button
                                    size="sm"
                                    colorScheme="blue"
                                    leftIcon={<FiDownload />}
                                    onClick={() =>
                                      handleDownload(result.output_file || result.download_url.split('/').pop())
                                    }
                                  >
                                    Download
                                  </Button>
                                )}
                              </HStack>
                              {result.error && (
                                <Text fontSize="sm" color="red.600" mt={2}>
                                  Error: {result.error}
                                </Text>
                              )}
                            </Box>
                          ))}
                        </VStack>
                      </CardBody>
                    </Card>
                  )}
                </VStack>
              </TabPanel>

              {/* Formats Tab */}
              <TabPanel>
                <Card>
                  <CardHeader>
                    <Heading size="md">Supported Formats</Heading>
                  </CardHeader>
                  <CardBody>
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                      {[
                        { format: 'PDF', desc: 'Portable Document Format', ext: '.pdf' },
                        { format: 'DOCX', desc: 'Microsoft Word Document', ext: '.docx' },
                        { format: 'XLSX', desc: 'Microsoft Excel Spreadsheet', ext: '.xlsx' },
                        { format: 'CSV', desc: 'Comma-Separated Values', ext: '.csv' },
                        { format: 'JSON', desc: 'JavaScript Object Notation', ext: '.json' },
                        { format: 'TXT', desc: 'Plain Text File', ext: '.txt' },
                      ].map((item) => (
                        <Card key={item.format} variant="outline">
                          <CardBody>
                            <VStack align="start" spacing={2}>
                              <Badge colorScheme="blue" fontSize="md">
                                {item.format}
                              </Badge>
                              <Text fontSize="sm" color="gray.600">
                                {item.desc}
                              </Text>
                              <Text fontSize="xs" color="gray.500">
                                Extension: {item.ext}
                              </Text>
                            </VStack>
                          </CardBody>
                        </Card>
                      ))}
                    </SimpleGrid>

                    <Divider my={6} />

                    <Box>
                      <Heading size="sm" mb={4}>
                        Conversion Statistics
                      </Heading>
                      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                        <Stat>
                          <StatLabel>Total Formats</StatLabel>
                          <StatNumber>6</StatNumber>
                          <StatHelpText>Supported file types</StatHelpText>
                        </Stat>
                        <Stat>
                          <StatLabel>Total Conversions</StatLabel>
                          <StatNumber>30</StatNumber>
                          <StatHelpText>Conversion pairs</StatHelpText>
                        </Stat>
                        <Stat>
                          <StatLabel>Quality Levels</StatLabel>
                          <StatNumber>3</StatNumber>
                          <StatHelpText>Low, Medium, High</StatHelpText>
                        </Stat>
                      </SimpleGrid>
                    </Box>
                  </CardBody>
                </Card>
              </TabPanel>

              {/* About Tab */}
              <TabPanel>
                <Card>
                  <CardHeader>
                    <Heading size="md">About Universal Document Converter</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack align="start" spacing={4}>
                      <Text>
                        Universal Document Converter is a powerful tool for converting documents
                        between multiple formats with high quality and ease of use.
                      </Text>

                      <Divider />

                      <Box>
                        <Heading size="sm" mb={2}>
                          Features
                        </Heading>
                        <VStack align="start" spacing={1}>
                          <Text>✓ 30+ conversion pairs</Text>
                          <Text>✓ High-quality conversions</Text>
                          <Text>✓ Batch processing support</Text>
                          <Text>✓ Fast and efficient</Text>
                          <Text>✓ Easy-to-use interface</Text>
                        </VStack>
                      </Box>

                      <Divider />

                      <Box>
                        <Heading size="sm" mb={2}>
                          Technology Stack
                        </Heading>
                        <Text>Backend: Python, FastAPI</Text>
                        <Text>Frontend: React, Chakra UI</Text>
                        <Text>Converters: PyPDF2, python-docx, pandas</Text>
                      </Box>

                      <Divider />

                      <Box>
                        <Text fontSize="sm" color="gray.600">
                          Version 1.0.0 | © 2024 Universal Document Converter
                        </Text>
                      </Box>
                    </VStack>
                  </CardBody>
                </Card>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
