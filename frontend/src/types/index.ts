export interface User {
  id: string;
  email: string;
  role: 'industry' | 'artisan' | 'admin';
  name: string;
  companyName?: string;
  gstNumber?: string;
  location?: string;
  isVerified: boolean;
  createdAt: string;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  loading: boolean;
  isAuthenticated: boolean;
}

export interface RegisterData {
  email: string;
  password: string;
  role: 'industry' | 'artisan';
  name: string;
  companyName?: string;
  gstNumber?: string;
  location?: string;
}

export interface Material {
  id: string;
  name: string;
  category: string;
  quantity: number;
  unit: string;
  location: string;
  price: number;
  description: string;
  images: string[];
  ownerId: string;
  status: 'available' | 'reserved' | 'sold';
  createdAt: string;
}

export interface Request {
  id: string;
  materialId: string;
  requesterId: string;
  ownerId: string;
  quantity: number;
  message: string;
  status: 'pending' | 'accepted' | 'rejected' | 'completed';
  createdAt: string;
  updatedAt: string;
}

export interface Transaction {
  id: string;
  requestId: string;
  amount: number;
  status: 'pending' | 'completed' | 'failed';
  paymentMethod: string;
  createdAt: string;
}

export interface AnalyticsData {
  totalTransactions: number;
  totalRevenue: number;
  materialsSold: number;
  carbonFootprintSaved: number;
  monthlyData: {
    month: string;
    transactions: number;
    revenue: number;
  }[];
}