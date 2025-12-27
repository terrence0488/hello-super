-- =============================================================================
-- Supabase Database Setup Script for Hello Super
-- =============================================================================
-- Run this script in your Supabase SQL Editor:
-- https://supabase.com/dashboard/project/_/sql/new
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Create the tasks table
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT false,
    attachment_path TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Add comment for documentation
COMMENT ON TABLE public.tasks IS 'User tasks for the Hello Super demo app';

-- -----------------------------------------------------------------------------
-- 2. Create indexes for performance
-- -----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON public.tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON public.tasks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tasks_is_completed ON public.tasks(is_completed);

-- -----------------------------------------------------------------------------
-- 3. Enable Row Level Security (RLS)
-- -----------------------------------------------------------------------------

ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;

-- -----------------------------------------------------------------------------
-- 4. Create RLS Policies
-- -----------------------------------------------------------------------------

-- Policy: Users can view their own tasks
CREATE POLICY "Users can view own tasks" 
    ON public.tasks 
    FOR SELECT 
    USING (auth.uid() = user_id);

-- Policy: Users can create their own tasks
CREATE POLICY "Users can create own tasks" 
    ON public.tasks 
    FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own tasks
CREATE POLICY "Users can update own tasks" 
    ON public.tasks 
    FOR UPDATE 
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can delete their own tasks
CREATE POLICY "Users can delete own tasks" 
    ON public.tasks 
    FOR DELETE 
    USING (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 5. Create updated_at trigger function
-- -----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to auto-update updated_at
DROP TRIGGER IF EXISTS update_tasks_updated_at ON public.tasks;
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON public.tasks
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- -----------------------------------------------------------------------------
-- 6. Create Storage Bucket for attachments (Phase 4)
-- -----------------------------------------------------------------------------
-- Note: Storage buckets are created via the Supabase Dashboard or API,
-- not via SQL. Go to Storage in your Supabase Dashboard and create a bucket
-- named 'task-attachments' with the following settings:
--   - Public: false (private bucket)
--   - File size limit: 5MB
--   - Allowed MIME types: image/*, application/pdf

-- Storage RLS policies (apply via Dashboard > Storage > Policies):
-- 
-- SELECT policy (view files):
--   auth.uid()::text = (storage.foldername(name))[1]
--
-- INSERT policy (upload files):
--   auth.uid()::text = (storage.foldername(name))[1]
--
-- DELETE policy (remove files):
--   auth.uid()::text = (storage.foldername(name))[1]

-- -----------------------------------------------------------------------------
-- Done! Your database is now set up for Hello Super.
-- -----------------------------------------------------------------------------

-- Verify setup
SELECT 
    'tasks' as table_name,
    (SELECT count(*) FROM information_schema.tables WHERE table_name = 'tasks') as exists,
    (SELECT count(*) FROM pg_policies WHERE tablename = 'tasks') as policy_count;

