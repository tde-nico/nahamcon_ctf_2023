package com.nahamcon2023.jninjaspeak.databinding;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import androidx.viewbinding.ViewBinding;
import androidx.viewbinding.ViewBindings;
import com.nahamcon2023.jninjaspeak.R;

/* loaded from: classes4.dex */
public final class ActivityMainBinding implements ViewBinding {
    private final LinearLayout rootView;
    public final Button translateButton;
    public final EditText translateInput;

    private ActivityMainBinding(LinearLayout rootView, Button translateButton, EditText translateInput) {
        this.rootView = rootView;
        this.translateButton = translateButton;
        this.translateInput = translateInput;
    }

    @Override // androidx.viewbinding.ViewBinding
    public LinearLayout getRoot() {
        return this.rootView;
    }

    public static ActivityMainBinding inflate(LayoutInflater inflater) {
        return inflate(inflater, null, false);
    }

    public static ActivityMainBinding inflate(LayoutInflater inflater, ViewGroup parent, boolean attachToParent) {
        View root = inflater.inflate(R.layout.activity_main, parent, false);
        if (attachToParent) {
            parent.addView(root);
        }
        return bind(root);
    }

    public static ActivityMainBinding bind(View rootView) {
        int id = R.id.translate_button;
        Button translateButton = (Button) ViewBindings.findChildViewById(rootView, R.id.translate_button);
        if (translateButton != null) {
            id = R.id.translate_input;
            EditText translateInput = (EditText) ViewBindings.findChildViewById(rootView, R.id.translate_input);
            if (translateInput != null) {
                return new ActivityMainBinding((LinearLayout) rootView, translateButton, translateInput);
            }
        }
        String missingId = rootView.getResources().getResourceName(id);
        throw new NullPointerException("Missing required view with ID: ".concat(missingId));
    }
}