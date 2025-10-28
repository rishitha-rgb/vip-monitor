import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/authService';

interface DashboardStats {
  total_materials?: number;
  available_materials?: number;
  total_requests?: number;
  pending_requests?: number;
  accepted_requests?: number;
  total_transactions?: number;
  total_revenue?: number;
  total_spent?: number;
}

interface DashboardData {
  user_type: 'industry' | 'artisan' | 'admin';
  stats: DashboardStats;
  recent_materials?: any[];
  recent_requests?: any[];
  available_materials?: any[];
  recent_users?: any[];
  recent_activities?: any;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/dashboard');
      setDashboardData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">{error}</p>
          <button
            onClick={fetchDashboardData}
            className="mt-2 btn-primary"
          >
            Retry
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">
              Welcome back, {user?.name}!
            </h1>
            <p className="text-gray-600 mt-1">
              {user?.role === 'industry' && 'Manage your materials and requests'}
              {user?.role === 'artisan' && 'Discover materials and track your requests'}
              {user?.role === 'admin' && 'Monitor platform activity and users'}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-500">
              {new Date().toLocaleDateString('en-IN', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </p>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {user?.role === 'industry' && (
            <>
              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-primary-100">
                    <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Total Materials</p>
                    <p className="text-2xl font-bold text-gray-800">{dashboardData?.stats.total_materials || 0}</p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-green-100">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Available</p>
                    <p className="text-2xl font-bold text-gray-800">{dashboardData?.stats.available_materials || 0}</p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-secondary-100">
                    <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Requests</p>
                    <p className="text-2xl font-bold text-gray-800">{dashboardData?.stats.total_requests || 0}</p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-yellow-100">
                    <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Revenue</p>
                    <p className="text-2xl font-bold text-gray-800">₹{(dashboardData?.stats.total_revenue || 0).toLocaleString('en-IN')}</p>
                  </div>
                </div>
              </div>
            </>
          )}

          {user?.role === 'artisan' && (
            <>
              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-primary-100">
                    <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">My Requests</p>
                    <p className="text-2xl font-bold text-gray-800">{dashboardData?.stats.total_requests || 0}</p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-green-100">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Accepted</p>
                    <p className="text-2xl font-bold text-gray-800">{dashboardData?.stats.accepted_requests || 0}</p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-secondary-100">
                    <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Available Materials</p>
                    <p className="text-2xl font-bold text-gray-800">{dashboardData?.stats.available_materials || 0}</p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="p-3 rounded-full bg-yellow-100">
                    <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Total Spent</p>
                    <p className="text-2xl font-bold text-gray-800">₹{(dashboardData?.stats.total_spent || 0).toLocaleString('en-IN')}</p>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Materials/Available Materials */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              {user?.role === 'industry' ? 'Recent Materials' : 'Available Materials'}
            </h3>
            <div className="space-y-3">
              {(user?.role === 'industry' ? dashboardData?.recent_materials : dashboardData?.available_materials)?.slice(0, 5).map((material: any) => (
                <div key={material.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-800">{material.name}</p>
                    <p className="text-sm text-gray-500">{material.category} • {material.location}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-800">₹{material.price}</p>
                    <p className="text-sm text-gray-500">{material.quantity} {material.unit}</p>
                  </div>
                </div>
              )) || (
                <p className="text-gray-500 text-center py-4">No materials found</p>
              )}
            </div>
          </div>

          {/* Recent Requests */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Requests</h3>
            <div className="space-y-3">
              {dashboardData?.recent_requests?.slice(0, 5).map((request: any) => (
                <div key={request.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-800">{request.material_name}</p>
                    <p className="text-sm text-gray-500">
                      {user?.role === 'industry' ? `From: ${request.requester_name}` : `To: ${request.owner_name}`}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      request.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      request.status === 'accepted' ? 'bg-green-100 text-green-800' :
                      request.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {request.status}
                    </span>
                    <p className="text-sm text-gray-500 mt-1">₹{request.total_amount?.toLocaleString('en-IN')}</p>
                  </div>
                </div>
              )) || (
                <p className="text-gray-500 text-center py-4">No requests found</p>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {user?.role === 'industry' && (
              <>
                <button className="btn-primary">
                  Add New Material
                </button>
                <button className="btn-outline">
                  View All Requests
                </button>
                <button className="btn-secondary">
                  Analytics Dashboard
                </button>
              </>
            )}
            {user?.role === 'artisan' && (
              <>
                <button className="btn-primary">
                  Browse Materials
                </button>
                <button className="btn-outline">
                  My Requests
                </button>
                <button className="btn-secondary">
                  Update Profile
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;