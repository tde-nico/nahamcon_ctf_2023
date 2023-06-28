package com.nahamcon2023.jninjaspeak;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;

/* compiled from: MainActivity.kt */
@Metadata(d1 = {"\u00000\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0002\u0018\u0000 \u00132\u00020\u0001:\u0001\u0013B\u0005¢\u0006\u0002\u0010\u0002J\u0012\u0010\t\u001a\u00020\n2\b\u0010\u000b\u001a\u0004\u0018\u00010\fH\u0014J\u0011\u0010\r\u001a\u00020\u000e2\u0006\u0010\u000f\u001a\u00020\u000eH\u0082 J\u000e\u0010\u0010\u001a\u00020\n2\u0006\u0010\u0011\u001a\u00020\u0012R\u001a\u0010\u0003\u001a\u00020\u0004X\u0086.¢\u0006\u000e\n\u0000\u001a\u0004\b\u0005\u0010\u0006\"\u0004\b\u0007\u0010\b¨\u0006\u0014"}, d2 = {"Lcom/nahamcon2023/jninjaspeak/MainActivity;", "Landroidx/appcompat/app/AppCompatActivity;", "()V", "translateInput", "Landroid/widget/EditText;", "getTranslateInput", "()Landroid/widget/EditText;", "setTranslateInput", "(Landroid/widget/EditText;)V", "onCreate", "", "savedInstanceState", "Landroid/os/Bundle;", "translate", "", "input", "translatePress", "v", "Landroid/view/View;", "Companion", "app_debug"}, k = 1, mv = {1, 8, 0}, xi = 48)
/* loaded from: classes3.dex */
public final class MainActivity extends AppCompatActivity {
    public static final Companion Companion = new Companion(null);
    public static String translateString;
    public EditText translateInput;

    private final native String translate(String str);

    public final EditText getTranslateInput() {
        EditText editText = this.translateInput;
        if (editText != null) {
            return editText;
        }
        Intrinsics.throwUninitializedPropertyAccessException("translateInput");
        return null;
    }

    public final void setTranslateInput(EditText editText) {
        Intrinsics.checkNotNullParameter(editText, "<set-?>");
        this.translateInput = editText;
    }

    /* JADX INFO: Access modifiers changed from: protected */
    @Override // androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        View findViewById = findViewById(R.id.translate_input);
        Intrinsics.checkNotNullExpressionValue(findViewById, "findViewById(R.id.translate_input)");
        setTranslateInput((EditText) findViewById);
    }

    public final void translatePress(View v) {
        Intrinsics.checkNotNullParameter(v, "v");
        Companion companion = Companion;
        companion.setTranslateString(getTranslateInput().getText().toString());
        translate(companion.getTranslateString());
        Toast toast = Toast.makeText(this, translate(companion.getTranslateString()), 0);
        toast.show();
    }

    /* compiled from: MainActivity.kt */
    @Metadata(d1 = {"\u0000\u0014\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0005\b\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002R\u001a\u0010\u0003\u001a\u00020\u0004X\u0086.¢\u0006\u000e\n\u0000\u001a\u0004\b\u0005\u0010\u0006\"\u0004\b\u0007\u0010\b¨\u0006\t"}, d2 = {"Lcom/nahamcon2023/jninjaspeak/MainActivity$Companion;", "", "()V", "translateString", "", "getTranslateString", "()Ljava/lang/String;", "setTranslateString", "(Ljava/lang/String;)V", "app_debug"}, k = 1, mv = {1, 8, 0}, xi = 48)
    /* loaded from: classes3.dex */
    public static final class Companion {
        public /* synthetic */ Companion(DefaultConstructorMarker defaultConstructorMarker) {
            this();
        }

        private Companion() {
        }

        public final String getTranslateString() {
            String str = MainActivity.translateString;
            if (str != null) {
                return str;
            }
            Intrinsics.throwUninitializedPropertyAccessException("translateString");
            return null;
        }

        public final void setTranslateString(String str) {
            Intrinsics.checkNotNullParameter(str, "<set-?>");
            MainActivity.translateString = str;
        }
    }

    static {
        System.loadLibrary("jninjaspeak");
    }
}