package androidx.startup;

import android.content.ComponentName;
import android.content.Context;
import android.content.pm.PackageManager;
import android.content.pm.ProviderInfo;
import android.os.Bundle;
import androidx.tracing.Trace;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/* loaded from: classes.dex */
public final class AppInitializer {
    private static final String SECTION_NAME = "Startup";
    private static volatile AppInitializer sInstance;
    private static final Object sLock = new Object();
    final Context mContext;
    final Set<Class<? extends Initializer<?>>> mDiscovered = new HashSet();
    final Map<Class<?>, Object> mInitialized = new HashMap();

    AppInitializer(Context context) {
        this.mContext = context.getApplicationContext();
    }

    public static AppInitializer getInstance(Context context) {
        if (sInstance == null) {
            synchronized (sLock) {
                if (sInstance == null) {
                    sInstance = new AppInitializer(context);
                }
            }
        }
        return sInstance;
    }

    static void setDelegate(AppInitializer delegate) {
        synchronized (sLock) {
            sInstance = delegate;
        }
    }

    public <T> T initializeComponent(Class<? extends Initializer<T>> component) {
        return (T) doInitialize(component);
    }

    public boolean isEagerlyInitialized(Class<? extends Initializer<?>> component) {
        return this.mDiscovered.contains(component);
    }

    /* JADX WARN: Multi-variable type inference failed */
    <T> T doInitialize(Class<? extends Initializer<?>> component) {
        Object result;
        synchronized (sLock) {
            result = (T) this.mInitialized.get(component);
            if (result == null) {
                result = (T) doInitialize(component, new HashSet());
            }
        }
        return (T) result;
    }

    private <T> T doInitialize(Class<? extends Initializer<?>> component, Set<Class<?>> initializing) {
        Object result;
        boolean isTracingEnabled = Trace.isEnabled();
        if (isTracingEnabled) {
            try {
                Trace.beginSection(component.getSimpleName());
            } finally {
                Trace.endSection();
            }
        }
        if (initializing.contains(component)) {
            String message = String.format("Cannot initialize %s. Cycle detected.", component.getName());
            throw new IllegalStateException(message);
        }
        if (!this.mInitialized.containsKey(component)) {
            initializing.add(component);
            Object instance = component.getDeclaredConstructor(new Class[0]).newInstance(new Object[0]);
            Initializer<?> initializer = (Initializer) instance;
            List<Class<? extends Initializer<?>>> dependencies = initializer.dependencies();
            if (!dependencies.isEmpty()) {
                for (Class<? extends Initializer<?>> clazz : dependencies) {
                    if (!this.mInitialized.containsKey(clazz)) {
                        doInitialize(clazz, initializing);
                    }
                }
            }
            result = (T) initializer.create(this.mContext);
            initializing.remove(component);
            this.mInitialized.put(component, result);
        } else {
            result = (T) this.mInitialized.get(component);
        }
        return (T) result;
    }

    /* JADX INFO: Access modifiers changed from: package-private */
    public void discoverAndInitialize() {
        try {
            try {
                Trace.beginSection(SECTION_NAME);
                ComponentName provider = new ComponentName(this.mContext.getPackageName(), InitializationProvider.class.getName());
                ProviderInfo providerInfo = this.mContext.getPackageManager().getProviderInfo(provider, 128);
                Bundle metadata = providerInfo.metaData;
                discoverAndInitialize(metadata);
            } catch (PackageManager.NameNotFoundException exception) {
                throw new StartupException(exception);
            }
        } finally {
            Trace.endSection();
        }
    }

    /* JADX WARN: Multi-variable type inference failed */
    void discoverAndInitialize(Bundle metadata) {
        String startup = this.mContext.getString(R.string.androidx_startup);
        if (metadata != null) {
            try {
                Set<Class<?>> initializing = new HashSet<>();
                Set<String> keys = metadata.keySet();
                for (String key : keys) {
                    String value = metadata.getString(key, null);
                    if (startup.equals(value)) {
                        Class<?> clazz = Class.forName(key);
                        if (Initializer.class.isAssignableFrom(clazz)) {
                            this.mDiscovered.add(clazz);
                        }
                    }
                }
                for (Class<? extends Initializer<?>> component : this.mDiscovered) {
                    doInitialize(component, initializing);
                }
            } catch (ClassNotFoundException exception) {
                throw new StartupException(exception);
            }
        }
    }
}